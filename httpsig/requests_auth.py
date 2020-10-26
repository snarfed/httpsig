import requests.auth
try:
    # Python 3
    from urllib.parse import urlparse
except ImportError:
    # Python 2
    from urlparse import urlparse

from .sign import HeaderSigner


class HTTPSignatureAuth(requests.auth.AuthBase):
    """
    Sign a request using the http-signature scheme.
    https://github.com/joyent/node-http-signature/blob/master/http_signing.md

    `key_id` is the mandatory label indicating to the server which secret to
      use secret is the filename of a pem file in the case of rsa, a password
      string in the case of an hmac algorithm
    `algorithm` is one of the six specified algorithms
      headers is a list of http headers to be included in the signing string,
      defaulting to "Date" alone.
    `sign_header`, optional, header used to include signature. defaults to
       'authorization'.
    """
    def __init__(self, key_id='', secret='', algorithm=None, headers=None,
                 sign_header='authorization'):
        headers = headers or []
        self.header_signer = HeaderSigner(
                                key_id=key_id, secret=secret,
                                algorithm=algorithm, headers=headers,
                                sign_header=sign_header)
        self.uses_host = 'host' in [h.lower() for h in headers]

    def __call__(self, r):
        headers = self.header_signer.sign(
                r.headers,
                # 'Host' header unavailable in request object at this point
                # if 'host' header is needed, extract it from the url
                host=urlparse(r.url).netloc if self.uses_host else None,
                method=r.method,
                path=r.path_url)
        r.headers.update(headers)
        return r
