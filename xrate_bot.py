import logging
from datetime import datetime
from pytz import timezone
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
'''
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
)
'''
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    CallbackContext,
)

from get_rates import (
    get_figi_price,
    get_all_figi_prices,
    chart_ticker_for_period,
    get_tickers_df,
)

from dbutils import create_tickers_table, get_figi_by_ticker

allowed_users = [1183558,]

def user_auth(func):
    def wrapper(*args):
        update = args[0]
        user_id = update.message.from_user.id
        if user_id not in allowed_users:
            logger.info(f'Access Denied')
            return
        else:
            return func(*args)

    return wrapper

def log(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Function {func.__name__} called")
        return func(*args, **kwargs)
    return wrapper



BOT_ENV = os.getenv('BOT_ENV')
TOKEN = os.getenv('TG_XRATE_TOKEN')

if BOT_ENV == 'prod':
    APP_NAME = 'https://gapon.me/'
    PORT = int(os.environ.get('PORT', '8443'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

kb = [[
    InlineKeyboardButton('CNY', callback_data='CNY'),
    InlineKeyboardButton('USD', callback_data='USD'),
    #InlineKeyboardButton('BTC', callback_data='BTC'),
    ],
    [InlineKeyboardButton('Get All', callback_data='ALL'),]]

@user_auth
@log
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = kb
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose a currency', reply_markup=reply_markup )




@log
async def get_rates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = kb
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.data == 'ALL':
        rates = get_all_figi_prices()
    else:
        rates = f'{query.data}: {get_figi_price(get_figi_by_ticker(query.data))}'

    await query.answer()
    await query.edit_message_text(rates)
    await query.message.reply_text('Choose a currency', reply_markup=reply_markup)

@user_auth
def set(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    ticker = context.args[0]
    bottom_price = context.args[1]
    upper_price = context.args[2]
    job_context = {'chat_id': chat_id, 'ticker': ticker, 'bottom_price': bottom_price, 'upper_price': upper_price}
    context.job_queue.run_repeating(alarm, 60, context=job_context, name=str(chat_id))
    text = f'{ticker} job for bottom_price: {bottom_price} and upper_price: {upper_price} is set'
    update.message.reply_text(text)

def alarm(context: CallbackContext):
    job = context.job
    ticker = job.context['ticker']
    figi = get_figi_by_ticker(ticker)
    bottom_price = float(job.context['bottom_price'])
    upper_price = float(job.context['upper_price'])
    rate = get_figi_price(figi)
    if rate:
        if rate >= upper_price:
            text = f"🟢 {ticker} reached upper price of {upper_price}. Current price is *{rate}*"
            context.bot.send_message(job.context['chat_id'],text=text, parse_mode= 'Markdown')
        elif rate <= bottom_price:
            text = f"🔴 {ticker} reached bottom price of {bottom_price}. Current price is *{rate}*"
            context.bot.send_message(job.context['chat_id'], text=text, parse_mode= 'Markdown')

def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

@user_auth
def unset(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Job successfully cancelled!' if job_removed else 'You have no active jobs.'
    update.message.reply_text(text)

@user_auth
async def chart(update: Update, context: CallbackContext)->None:
    """
    Outputs a ticker close price chart for the period

    /chart {ticker} {period}
    arg[0] - figi_name
    arg[1] - period 30/90/360 days
    """

    ticker = context.args[0]
    period = int(context.args[1])

    chart_ticker_for_period(ticker, period)

    chat_id = update.message.chat_id
    await context.bot.send_photo(chat_id, open('output.png', 'rb'))


def main() -> None:
    # Creating db with ticker-figi
    tickers_df = get_tickers_df()
    create_tickers_table(tickers_df)

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(get_rates))
    application.add_handler(CommandHandler('chart', chart))

    #dispatcher.add_handler(CommandHandler('set', set))
    #dispatcher.add_handler(CommandHandler('unset', unset))


    # Run the bot until the user presses Ctrl-C
    if BOT_ENV == 'prod':
        application.run_webhook(
            listen='0.0.0.0',
            port=5000,
            url_path=TOKEN,
            #secret_token='ASecretTokenIHaveChangedByNow',
            webhook_url='https://gapon.me/'+TOKEN,
            #cert='cert.pem'
        )
    else:
        application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == '__main__':
    main()
