import logging

from telegram.ext import CommandHandler, MessageHandler, Updater, Filters

from bot import commands, config

logging.basicConfig(level=logging.INFO)


def main():
    book_bot = Updater(config.api_key, use_context=True, request_kwargs=config.proxy)

    bd = book_bot.dispatcher
    bd.add_handler(MessageHandler(Filters.text, commands.search))

    logging.info('Бот стартовал;')

    book_bot.start_polling()

    book_bot.idle()
