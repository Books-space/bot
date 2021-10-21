from bot.client.client import BooksMarketplaceClient as Client


def hello(update, context):
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')


def search(update, context):
    if context.args:
        books_client = Client()
        phrase = ' '.join(context.args)
        books_client.search(phrase)
    else:
        update.message.reply_text(
            'Привет, пользователь! Ты не указал интересующую слово или фразу для поиска!',
        )
