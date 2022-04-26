import logging
from datetime import datetime
from pytz import timezone
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    ConversationHandler,
    MessageHandler,
)
from get_rates import ticker_price_on_date


BOT_ENV = os.getenv('BOT_ENV')
TOKEN = os.getenv('TG_XRATE_TOKEN')
USD_TICKER = 'USD000UTSTOM'

if BOT_ENV == 'prod':
    APP_NAME = 'https://xrate-bot.herokuapp.com/'
    PORT = int(os.environ.get('PORT', '8443'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton('USD', callback_data='USD')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Test', reply_markup=reply_markup )

def get_rates(update: Update, context: CallbackContext):
    current_time = datetime.now(timezone('UTC'))
    usd_rub = str(ticker_price_on_date(USD_TICKER, current_time))
    query = update.callback_query
    keyboard = [[InlineKeyboardButton('USD', callback_data='USD')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.answer()
    query.delete_message()
    query.message.reply_text(usd_rub, reply_markup=reply_markup)


def main() -> None:

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
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