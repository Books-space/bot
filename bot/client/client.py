import logging

import httpx


class BooksMarketplaceClient:  # noqa: WPS306

    ok_status_code = 201
    timeout = 5

    def __init__(self, backend_url: str):
        self.url = '{0}{1}'.format(backend_url, '/api/v1/books/')

    def search(self, phrase) -> str:
        parameter = {'search': phrase}
        try:  # noqa: WPS229
            response = httpx.get(self.url, params=parameter)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            logging.exception(exc)
            raise RuntimeError
        logging.debug(response.json())
        return response.json()
