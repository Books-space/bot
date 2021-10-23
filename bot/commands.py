import logging

from telegram import ParseMode

from bot.client.client import BooksMarketplaceClient as Client
from bot.config import backend_url
from bot.tools.json_telegram import convert_to_messages

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def hello(update, context):
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')


def search(update, context):
    if update.message.text:
        books_client = Client(backend_url)
        phrase = update.message.text
        response = books_client.search(phrase)
        logger.debug(response)
        logger.debug(type(response))
        tm_messages = convert_to_messages(response)
        if not tm_messages:
            update.message.reply_text('Книг с такой строкой в названии или имени автора нет.')
        for msg in tm_messages:
            update.message.reply_text(text=msg, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(
            'Привет, пользователь! Ты не указал интересующую слово или фразу для поиска!',
        )
