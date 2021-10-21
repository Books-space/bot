import httpx


class BooksMarketplaceClient:  # noqa: WPS306

    url = 'http://127.0.0.1:5000/api/v1/books/'
    ok_status_code = 201
    timeout = 5

    def search(self, phrase) -> str:
        parameter = {'search': phrase}
        return httpx.get(self.url, params=parameter).json()
