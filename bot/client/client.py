import httpx


class BooksMarketplaceClient:  # noqa: WPS306

    ok_status_code = 201
    timeout = 5

    def __init__(self, backend_url: str):
        self.url = backend_url

    def search(self, phrase) -> str:
        parameter = {'search': phrase}
        return httpx.get(self.url, params=parameter).json()
