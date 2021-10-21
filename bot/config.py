import os

api_key = os.environ['API_KEY']
proxy_url = os.environ['PROXY_URL']
proxy_username = os.environ['PROXY_USERNAME']
proxy_password = os.environ['PROXY_PASSW']


proxy = {
    'proxy_url': proxy_url,
    'urllib3_proxy_kwargs':
    {
        'username': proxy_username,
        'password': proxy_password,
    },
}
