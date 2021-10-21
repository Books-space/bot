import logging

from bot.tools.schemes import Book

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


MESSAGE_TEMPLATE = """
        <i>Книга {0}</i>


        Название:
        <b><strong>{1}</strong></b>

        Автор: <b><strong>{2}</strong></b>



        Аннотация: <code>{6}</code>



        Издательство: {3}

        Год издания: {4}

        ISBN: {5}


        Обложка:
        <a href="{7}">&#8204;</a>
"""


def convert_to_messages(response: list[str]) -> list[str]:
    tm_messages = []
    for result_num, book_str in enumerate(response, start=1):
        book = Book(**book_str)
        msg = MESSAGE_TEMPLATE.format(
            result_num,
            book.title,
            book.author,
            book.publisher,
            book.year,
            book.isbn,
            book.annotation,
            book.cover,
        )
        tm_messages.append(msg)
    return tm_messages
