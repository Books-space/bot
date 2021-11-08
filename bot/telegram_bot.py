import logging

from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater

from bot import commands, config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    book_bot = Updater(config.api_key, use_context=True, request_kwargs=config.proxy)

    bot_dispatcher = book_bot.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', commands.add)],
        states={
            commands.ID: [MessageHandler(Filters.text, commands.get_id)],
            commands.TITLE: [MessageHandler(Filters.text, commands.get_title)],
            commands.AUTHOR: [
                CommandHandler('skip', commands.skip_author),
                MessageHandler(Filters.text, commands.get_author),
            ],
            commands.PUBLISHER: [
                CommandHandler('skip', commands.skip_publisher),
                MessageHandler(Filters.text, commands.get_publisher),
            ],
            commands.ISBN: [MessageHandler(Filters.text, commands.get_isbn)],
            commands.YEAR: [MessageHandler(Filters.text, commands.get_year)],
            commands.COVER: [MessageHandler(Filters.text, commands.get_cover)],
            commands.ANNOTATION: [
                CommandHandler('skip', commands.skip_annotation),
                MessageHandler(Filters.text, commands.get_annotation),
            ],
            commands.NEW_ISBN: [MessageHandler(Filters.text, commands.get_another_isbn)],
        },
        fallbacks=[CommandHandler('cancel', commands.cancel_book_add)],
    )

    bot_dispatcher.add_handler(CommandHandler('start', commands.hello))
    bot_dispatcher.add_handler(conv_handler)
    bot_dispatcher.add_handler(MessageHandler(Filters.text, commands.search))

    logger.info('Бот стартовал;')

    book_bot.start_polling()

    book_bot.idle()
