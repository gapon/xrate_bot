import logging
from datetime import datetime
from pytz import timezone
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
)
from get_rates import get_figi_price, get_all_figi_prices, figi_dict, get_candles_for_period, create_candles_df, plot_candles
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
import seaborn as sns


BOT_ENV = os.getenv('BOT_ENV')
TOKEN = os.getenv('TG_XRATE_TOKEN')

if BOT_ENV == 'prod':
    APP_NAME = 'https://gapon.me/'
    PORT = int(os.environ.get('PORT', '8443'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

kb = [[
    InlineKeyboardButton('CNY', callback_data='CNY'),
    InlineKeyboardButton('TMOS', callback_data='TMOS'),
    InlineKeyboardButton('USD', callback_data='USD'),
    #InlineKeyboardButton('BTC', callback_data='BTC'),
    ],
    [InlineKeyboardButton('Get All', callback_data='ALL'),]]

def start(update: Update, context: CallbackContext):
    keyboard = kb
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose a currency', reply_markup=reply_markup )

def get_rates(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = kb
    reply_markup = InlineKeyboardMarkup(keyboard)


    if query.data == 'ALL':
        rates = get_all_figi_prices()
    else:
        rates = f'{query.data}: {get_figi_price(figi_dict[query.data])}'
        

    query.answer()

    query.edit_message_text(rates)
    query.message.reply_text('Choose a currency', reply_markup=reply_markup)

def set(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    figi_name = context.args[0]
    bottom_price = context.args[1] 
    upper_price = context.args[2]
    job_context = {'chat_id': chat_id, 'figi_name': figi_name, 'bottom_price': bottom_price, 'upper_price': upper_price}
    context.job_queue.run_repeating(alarm, 60, context=job_context, name=str(chat_id))
    text = f'{figi_name} job for bottom_price: {bottom_price} and upper_price: {upper_price} is set'
    update.message.reply_text(text)

def alarm(context: CallbackContext):
    job = context.job
    figi_name = job.context['figi_name']
    figi = figi_dict[figi_name]
    bottom_price = float(job.context['bottom_price'])
    upper_price = float(job.context['upper_price'])
    rate = get_figi_price(figi)
    if rate:
        if rate >= upper_price:
            text = f"🟢 {figi_name} reached upper price of {upper_price}. Current price is *{rate}*"
            context.bot.send_message(job.context['chat_id'],text=text, parse_mode= 'Markdown')
        elif rate <= bottom_price:
            text = f"🔴 {figi_name} reached bottom price of {bottom_price}. Current price is *{rate}*"
            context.bot.send_message(job.context['chat_id'], text=text, parse_mode= 'Markdown')

def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def unset(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Job successfully cancelled!' if job_removed else 'You have no active jobs.'
    update.message.reply_text(text)

def graph(update: Update, context: CallbackContext)->None:
    """
    Outputs a ticker close price chart for the period

    /graph {ticker} {period}
    arg[0] - figi_name
    arg[1] - period 30/90/360 days
    """

    figi_name = context.args[0]
    figi = figi_dict[figi_name]
    period = int(context.args[1])

    canles = get_candles_for_period(figi, period)
    df = create_candles_df(canles)

    plt.figure(figsize=(10,5))
    ax = sns.lineplot(df, x=df['date'], y=df['close'])
    plt.savefig('output.png')

    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id, open('output.png', 'rb'))


def main() -> None:

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('set', set))
    dispatcher.add_handler(CommandHandler('unset', unset))
    dispatcher.add_handler(CommandHandler('graph', graph))
    dispatcher.add_handler(CallbackQueryHandler(get_rates))

    if BOT_ENV == 'prod':
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN,
                              webhook_url = APP_NAME + TOKEN)
    else:
        updater.start_polling(timeout=10)

    updater.idle()


if __name__ == '__main__':
    main()