from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    year: int
    isbn: str
    cover: str
    annotation: str
