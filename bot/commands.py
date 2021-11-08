import logging

from telegram import ParseMode
from telegram.ext import ConversationHandler

from bot.client.client import BooksMarketplaceClient as Client
from bot.config import backend_url
from bot.tools.json_telegram import convert_to_messages
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


ID, TITLE, AUTHOR, PUBLISHER, ISBN, YEAR, COVER, ANNOTATION, NEW_ISBN = range(9)


def hello(update, context):
    update.message.reply_text('Привет, пользователь! Это справочника'
    ' книг Booksmarket. Чтобы искать книги по строке в названии и имени автора просто набери '
    'эту строку.\nЧтобы добавить книгу набери /add')


def search(update, context):
    try:
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
    except Exception as exc:
        logging.exception(exc)
        update.message.reply_text(
            'Ой, у нас что-то пошло не так. Попробуй, пожалуйста, поискать книги чуть позже.',
        )


def add(update, _):
    update.message.reply_text(
        'Привет. Приступим к добавлению новой книги в наш справочник. '
        'Какой внешний id (целое число) ей присвоим?')
    return ID


def get_id(update, context):
    user = update.message.from_user
    context.user_data['book_id'] = update.message.text
    logger.info("Пользователь %s ввёл id книги %s", user.first_name, context.user_data['book_id'])
    update.message.reply_text(
        f'OK. Внешний id книги "{context.user_data["book_id"]}" принят;\n'
        'Теперь введи название книги.')
    return TITLE


def get_title(update, context):
    user = update.message.from_user
    context.user_data['book_title'] = update.message.text
    logger.info("Пользователь %s ввёл название книги %s", user.first_name, context.user_data['book_title'])
    update.message.reply_text(f'OK. Название "{context.user_data["book_title"]}" принято; Теперь введи автора книги или '
        '/skip чтобы пропустить шаг.')
    return AUTHOR


def get_author(update, context):
    user = update.message.from_user
    context.user_data['book_author'] = update.message.text
    logger.info("Пользователь %s ввёл автора книги %s", user.first_name, context.user_data['book_author'])
    update.message.reply_text(f'OK. Автор "{context.user_data["book_author"]}" принят; Теперь введи издательство книги'
        'или /skip чтобы пропустить.')
    return PUBLISHER


def skip_author(update, context):
    user = update.message.from_user
    context.user_data['book_author'] = None
    logger.info("Пользователь %s ввёл пропустил ввод автора книги", user.first_name)
    update.message.reply_text(f'OK. Автора пропустили; Теперь введи издательство книги '
        'или /skip чтобы пропустить.')
    return PUBLISHER


def get_publisher(update, context):
    user = update.message.from_user
    context.user_data['book_publisher'] = update.message.text
    logger.info("Пользователь %s ввёл издательство книги %s", user.first_name, context.user_data['book_publisher'],)
    update.message.reply_text(f'OK. Издательство "{context.user_data["book_publisher"]}" принято; Теперь введи ISBN')
    return ISBN


def skip_publisher(update, context):
    user = update.message.from_user
    context.user_data['book_publisher'] = None
    logger.info("Пользователь %s пропустил ввод издательства книги", user.first_name)
    update.message.reply_text(f'OK. Издательство пропустили; Теперь введи ISBN')
    return ISBN


def get_isbn(update, context):
    user = update.message.from_user
    context.user_data['book_isbn'] = update.message.text
    logger.info("Пользователь %s ввёл ISBN книги %s", user.first_name, context.user_data['book_isbn'])
    update.message.reply_text(f'OK. ISBN "{context.user_data["book_isbn"]}" принят; Теперь введи год издания книги')
    return YEAR


def get_year(update, context):
    user = update.message.from_user
    context.user_data['book_year'] = update.message.text
    logger.info("Пользователь %s ввёл год выпуска книги %s", user.first_name, context.user_data['book_year'])
    update.message.reply_text(f'OK. Год выпуска книги "{context.user_data["book_year"]}" принят; Теперь введи URL '
    'изображения обложки книги')
    return COVER


def get_cover(update, context):
    user = update.message.from_user
    context.user_data['book_cover'] = update.message.text
    logger.info("Пользователь %s ввёл URL обложки книги %s", user.first_name, context.user_data['book_cover'])
    update.message.reply_text(f'OK. URL обложки книги "{context.user_data["book_cover"]}" принят; Теперь'
    ' введи аннотацию книги или /skip чтобы пропустить')
    return ANNOTATION


def cancel_book_add(update, context):
    user = update.message.from_user
    logger.info("Пользователь %s отменил добавление книги", user.first)
    update.message.reply_text('Отменяем добавление текущей книги.')
    logger.info("Отмена сохранения книги:")
    logger.info("\nid: %s,\ntitle: %s,\nauthor: %s,\npublisher: %s,\nisbn:%s,\nyear: %s,\ncover: %s,\nannotation: %s" % (
        context.user_data['book_id'],
        context.user_data['book_title'],
        context.user_data['book_author'],
        context.user_data['book_publisher'],
        context.user_data['book_isbn'],
        context.user_data['book_year'],
        context.user_data['book_cover'],
        context.user_data['book_annotation'],
    )
    )
    return ConversationHandler.END


def get_annotation(update, context):
    user = update.message.from_user
    context.user_data['book_annotation'] = update.message.text
    logger.info("Пользователь %s ввёл аннотацию книги %s", user.first_name, context.user_data['book_annotation'])
    update.message.reply_text(f'OK. Аннотация книги "{context.user_data["book_annotation"]}" принята; Сохраняем книгу.')
    logger.info("Сохранение книги:")
    logger.info("id: %s,\ntitle: %s,\nauthor: %s,\npublisher: %s,\nisbn:%s,\nyear: %s,\ncover: %s,\nannotation: %s" % (
        context.user_data['book_id'],
        context.user_data['book_title'],
        context.user_data['book_author'],
        context.user_data['book_publisher'],
        context.user_data['book_isbn'],
        context.user_data['book_year'],
        context.user_data['book_cover'],
        context.user_data['book_annotation'],
    )
    )
    book_data = {
        'id': context.user_data['book_id'],
        'title': context.user_data['book_title'],
        'author': context.user_data['book_author'],
        'publisher': context.user_data['book_publisher'],
        'isbn': context.user_data['book_isbn'],
        'year': context.user_data['book_year'],
        'cover': context.user_data['book_cover'],
        'annotation': context.user_data['book_annotation'],
    }
    return send_book_to_backend(update, book_data)


def skip_annotation(update, context):
    user = update.message.from_user
    context.user_data['book_annotation'] = None
    logger.info("Пользователь %s пропустил ввод аннотации книги", user.first_name)
    update.message.reply_text(f'OK. Аннотацию книги пропустили; Сохраняем книгу.')
    logger.info("Сохранение книги:")
    logger.info("id: %s,\ntitle: %s,\nauthor: %s,\npublisher: %s,\nisbn:%s,\nyear: %s,\ncover: %s,\nannotation: %s" % (
        context.user_data['book_id'],
        context.user_data['book_title'],
        context.user_data['book_author'],
        context.user_data['book_publisher'],
        context.user_data['book_isbn'],
        context.user_data['book_year'],
        context.user_data['book_cover'],
        context.user_data['book_annotation'],
    )
    )
    book_data = {
        'id': context.user_data['book_id'],
        'title': context.user_data['book_title'],
        'author': context.user_data['book_author'],
        'publisher': context.user_data['book_publisher'],
        'isbn': context.user_data['book_isbn'],
        'year': context.user_data['book_year'],
        'cover': context.user_data['book_cover'],
        'annotation': context.user_data['book_annotation'],
    }
    return send_book_to_backend(update, book_data)


def get_another_isbn(update, context):
    user = update.message.from_user
    context.user_data['book_isbn'] = update.message.text
    logger.info("Пользователь %s ввёл новый ISBN книги %s", user.first_name, context.user_data['book_isbn'])
    update.message.reply_text(f'OK. ISBN "{context.user_data["book_isbn"]}" принят;')
    logger.info("Сохранение книги:")
    logger.info("id: %s,\ntitle: %s,\nauthor: %s,\npublisher: %s,\nisbn:%s,\nyear: %s,\ncover: %s,\nannotation: %s" % (
        context.user_data['book_id'],
        context.user_data['book_title'],
        context.user_data['book_author'],
        context.user_data['book_publisher'],
        context.user_data['book_isbn'],
        context.user_data['book_year'],
        context.user_data['book_cover'],
        context.user_data['book_annotation'],
    )
    )
    book_data = {
        'id': context.user_data['book_id'],
        'title': context.user_data['book_title'],
        'author': context.user_data['book_author'],
        'publisher': context.user_data['book_publisher'],
        'isbn': context.user_data['book_isbn'],
        'year': context.user_data['book_year'],
        'cover': context.user_data['book_cover'],
        'annotation': context.user_data['book_annotation'],
    }
    return send_book_to_backend(update, book_data)


def send_book_to_backend(update, book_dict):
    try:
        books_client = Client(backend_url)
        response = books_client.add(book_dict)
        logger.debug(response)
        logger.debug(type(response))
    except httpx.RemoteProtocolError as exc:
        logger.debug(exc)
        update.message.reply_text(
            'В нашем справочнике уже есть книга с таким названием. Попробуй, пожалуйста, задать другой ISBN или набери /cancel для отмены.',
        )
        return NEW_ISBN
    except Exception as exc:
        logging.exception(exc)
        update.message.reply_text(
            'Ой, у нас что-то пошло не так. Попробуй, пожалуйста, добавить книгу чуть позже.',
        )
    update.message.reply_text('Поздравляю! Заданная тобой книга сохранена в справочнике!')
    return ConversationHandler.END
