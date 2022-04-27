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
from get_rates import get_usd_rate, get_btc_rate


BOT_ENV = os.getenv('BOT_ENV')
TOKEN = os.getenv('TG_XRATE_TOKEN')

if BOT_ENV == 'prod':
    APP_NAME = 'https://xrate-bot.herokuapp.com/'
    PORT = int(os.environ.get('PORT', '8443'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton('USD', callback_data='USD'), InlineKeyboardButton('BTC', callback_data='BTC')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose a currency', reply_markup=reply_markup )

def get_rates(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton('USD', callback_data='USD'), InlineKeyboardButton('BTC', callback_data='BTC')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.data == 'USD':
        rate = get_usd_rate()
    elif query.data == 'BTC':
        rate = get_btc_rate()

    query.answer()

    query.edit_message_text(f'{query.data}: {rate}')
    query.message.reply_text('Choose a currency', reply_markup=reply_markup)

def set(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    bottom_price = context.args[0] 
    upper_price = context.args[1]
    job_context = {'chat_id': chat_id, 'bottom_price': bottom_price, 'upper_price': upper_price}
    context.job_queue.run_repeating(alarm, 5, context=job_context, name=str(chat_id))
    text = f'Job for bottom_price: {bottom_price} and upper_price: {upper_price} is set'
    update.message.reply_text(text)

def alarm(context: CallbackContext):
    job = context.job
    bottom_price = float(job.context['bottom_price'])
    upper_price = float(job.context['upper_price'])
    rate = get_usd_rate()
    if rate:
        if rate >= upper_price:
            text = f'🔺 Reached upper price of {upper_price}. Current price is {rate}'
            context.bot.send_message(job.context['chat_id'],text=text)
        elif rate <= bottom_price:
            text = f'🔻 Reached bottom price of {bottom_price}. Current price is {rate}'
            context.bot.send_message(job.context['chat_id'], text=text)

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



def main() -> None:

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('set', set))
    dispatcher.add_handler(CommandHandler('unset', unset))
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