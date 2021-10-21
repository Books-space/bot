import logging

from telegram.ext import CommandHandler, Updater

from bot import commands, config

logging.basicConfig(level=logging.INFO)


def main():
    book_bot = Updater(config.api_key, use_context=True, request_kwargs=config.proxy)

    bb = book_bot.dispatcher
    bb.add_handler(CommandHandler('start', commands.hello))
    bb.add_handler(CommandHandler('search', commands.search))

    logging.info('Бот стартовал;')

    book_bot.start_polling()

    book_bot.idle()
