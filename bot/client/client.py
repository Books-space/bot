import httpx
import json


class BooksMarketplaceClient:  # noqa: WPS306

    ok_status_code = 201
    timeout = 5

    def __init__(self, backend_url: str):
        self.url = '{0}{1}'.format(backend_url, '/api/v1/books/')

    def search(self, phrase) -> str:
        parameter = {'search': phrase}
        response = httpx.get(self.url, params=parameter)
        response.raise_for_status()
        return response.json()

    def add(self, book_dict) -> str:
        response = httpx.post(self.url, json=book_dict)
        return response
