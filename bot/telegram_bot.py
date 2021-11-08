import logging

from telegram.ext import Filters, MessageHandler, Updater, ConversationHandler, CommandHandler

from bot import config

from bot.commands import (
    search,
    add,
    get_id,
    get_title,
    get_author,
    skip_author,
    get_publisher,
    skip_publisher,
    get_isbn,
    get_year,
    get_cover,
    get_annotation,
    skip_annotation,
    cancel_book_add,
    get_another_isbn,
    ID, TITLE, AUTHOR, PUBLISHER, ISBN, YEAR, COVER, ANNOTATION, NEW_ISBN,
    add_test_book,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)





def main():
    book_bot = Updater(config.api_key, use_context=True, request_kwargs=config.proxy)

    bot_dispatcher = book_bot.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add)],
        states={
            ID: [MessageHandler(Filters.text, get_id)],
            TITLE: [MessageHandler(Filters.text, get_title)],
            AUTHOR: [CommandHandler('skip', skip_author), MessageHandler(Filters.text, get_author)],
            PUBLISHER: [CommandHandler('skip', skip_publisher), MessageHandler(Filters.text, get_publisher)],
            ISBN: [MessageHandler(Filters.text, get_isbn)],
            YEAR: [MessageHandler(Filters.text, get_year)],
            COVER: [MessageHandler(Filters.text, get_cover)],
            ANNOTATION: [CommandHandler('skip', skip_annotation), MessageHandler(Filters.text, get_annotation)],
            NEW_ISBN: [MessageHandler(Filters.text, get_another_isbn)]
        },
        fallbacks=[CommandHandler('cancel', cancel_book_add)],
    )

    bot_dispatcher.add_handler(CommandHandler('test_add', add_test_book))
    bot_dispatcher.add_handler(conv_handler)
    bot_dispatcher.add_handler(MessageHandler(Filters.text, search))

    logger.info('Бот стартовал;')

    book_bot.start_polling()

    book_bot.idle()
