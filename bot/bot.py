import logging

from telegram.ext import Updater

from bot import bot, config


logging.basicConfig(level=logging.INFO)


def main():
    book_bot = Updater(config.api_key, use_context=True, request_kwargs=config.proxy)

    bb = book_bot.dispatcher
    bb.addHandler('Привет', bot.hello)

    logging.info('Бот стартовал;')

    book_bot.start_polling()

    book_bot.idle()
