import logging

from bot.tools.schemes import Book

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

SHORT_ANNOTATION_LEN = 273
MESSAGE_TEMPLATE = """<b><strong>{2}</strong></b>

<b><strong>{1}</strong></b>

{3}, {4}
<a href="{6}">&#8204;</a>
<code>{5}</code>"""


def straighten_author(inverted_author: str) -> str:
    splited_author = inverted_author.split()
    if len(splited_author) > 1:
        splited_author.append(splited_author.pop(0))
        straight_author = ' '.join(splited_author)
    else:
        straight_author = inverted_author
    return straight_author


def remove_author_from_title(title: str, author: str) -> str:
    if title.startswith(author):
        title = title.replace(author, '', 1)
        if title.startswith(': '):
            title = title.replace(': ', '', 1)
    return title


def shorten_annotation(annotation: str) -> str:
    if len(annotation) <= SHORT_ANNOTATION_LEN:
        return annotation
    return ('{0}...'.format(annotation[:SHORT_ANNOTATION_LEN]))


def convert_to_messages(response: list[str]) -> list[str]:
    tm_messages = []
    for result_num, book_str in enumerate(response, start=1):
        book = Book(**book_str)
        book.author = straighten_author(book.author)
        book.title = remove_author_from_title(book.title, book.author)
        book.annotation = shorten_annotation(book.annotation)
        msg = MESSAGE_TEMPLATE.format(
            result_num,
            book.title,
            book.author,
            book.publisher,
            book.year,
            book.annotation,
            book.cover,
        )
        tm_messages.append(msg)
    return tm_messages
