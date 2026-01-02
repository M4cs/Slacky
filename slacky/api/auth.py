from slack_sdk import WebClient

class CookieWebClient(WebClient):
    """WebClient that supports cookie-based authentication for xoxc tokens"""

    def __init__(self, token, cookies=None, **kwargs):
        # Pass cookies as headers
        headers = kwargs.pop('headers', {})
        if cookies:
            headers['Cookie'] = cookies
        super().__init__(token=token, headers=headers, **kwargs)
        self.cookies = cookies


def authenticate(config):
    try:
        token = config['token']
        # For xoxc- tokens, we need to include the d and d-s cookies for authentication
        if token.startswith('xoxc-') and 'd_cookie' in config:
            cookies = f'd={config["d_cookie"]}'
            if 'd_s_cookie' in config:
                cookies += f'; d-s={config["d_s_cookie"]}'
            client = CookieWebClient(
                token=token,
                cookies=cookies
            )
        else:
            client = WebClient(token=token)
        return client
    except:
        return None