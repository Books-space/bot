from typing import Dict
from pprint import pprint
import httpx


class BooksMarketplaceClient:

    url = 'http://127.0.0.1:5000/api/v1/books/'
    ok_status_code = 201
    timeout = 5

    # def encode(phrase: str) -> str:

    # def get_all_books(self) -> Dict:
    #     response = self._session.get(self.url, timeout=self.timeout)
    #     return response.json()

    def search(self, phrase) -> Dict:
        parameter = {'search': phrase}
        response = httpx.get(self.url, params=parameter)
        pprint(response.json())

    # def add_new_book(self, book_data: Dict):
    #     response = self._session.post(self.url, json=book_data, timeout=self.timeout)
    #     if response.status_code == self.ok_status_code:
    #         return response.json()
    #     raise ValueError('Wrong params. Response message: {0}'.format(response.json()))
