"""Pluggable auth and HTTP session for the f5-rest driver.

Private to device-drivers/f5-rest/ — not a shared library. Imported via:

    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from lib.rest import TokenAuth, OAuth2ClientCredentials, BasicAuth, BearerAuth, RestSession

Auth classes
------------
TokenAuth               POST to a token endpoint, attach result via a custom header.
                        Covers any vendor that issues opaque tokens (F5, Cisco DNA-C, etc.)
OAuth2ClientCredentials client_credentials grant → Authorization: Bearer {token}
                        Auto-refreshes before expiry.
BasicAuth               Authorization: Basic base64(user:pass) — stateless, no fetch.
BearerAuth              Pre-obtained static token from env var or config.

RestSession
-----------
Wraps requests with the chosen auth. Transparently retries once on 401 after
refreshing the token, so callers don't need to handle token expiry.
"""

import base64
import time

import requests
from requests.exceptions import HTTPError


# ---------------------------------------------------------------------------
# Auth strategies
# ---------------------------------------------------------------------------

class _BaseAuth:
    def headers(self) -> dict:
        raise NotImplementedError

    def refresh(self):
        """Re-fetch credentials. Called automatically on 401."""
        pass


class BasicAuth(_BaseAuth):
    """HTTP Basic Auth — Authorization: Basic base64(user:pass).

    Stateless — no token fetch needed.
    """
    def __init__(self, username: str, password: str):
        encoded = base64.b64encode(f"{username}:{password}".encode()).decode()
        self._header = {"Authorization": f"Basic {encoded}", "Content-Type": "application/json"}

    def headers(self) -> dict:
        return self._header


class BearerAuth(_BaseAuth):
    """Static pre-obtained Bearer token.

    Token comes from an env var or a config value — the driver is responsible
    for passing it in. No refresh logic; if it expires, restart the service.
    """
    def __init__(self, token: str):
        self._header = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def headers(self) -> dict:
        return self._header


class TokenAuth(_BaseAuth):
    """Generic token-endpoint auth.

    POSTs a JSON payload to a token URL, walks a dotted path in the response
    to extract the token value, and attaches it via a configurable header name.

    Covers any vendor with an opaque token flow, e.g.:
      F5:   POST /mgmt/shared/authn/login → token.token → X-F5-Auth-Token
      DNAC: POST /dna/system/api/v1/auth/token → Token → X-Auth-Token

    Args:
        token_url:   Full URL of the token endpoint.
        payload:     JSON body sent to the token endpoint.
        token_path:  Dotted key path to the token in the response JSON
                     (e.g. "token.token" for F5, "Token" for DNAC).
        header_name: Request header that carries the token (default: X-Auth-Token).
        verify_ssl:  Passed to requests.
        timeout:     Seconds before the token request times out.
    """
    def __init__(self, token_url: str, payload: dict, token_path: str,
                 header_name: str = "X-Auth-Token",
                 verify_ssl: bool = True, timeout: int = 15):
        self._url = token_url
        self._payload = payload
        self._path = token_path.split(".")
        self._header_name = header_name
        self._verify = verify_ssl
        self._timeout = timeout
        self._token = None

    def _fetch(self):
        r = requests.post(self._url, json=self._payload,
                          verify=self._verify, timeout=self._timeout)
        r.raise_for_status()
        data = r.json()
        for key in self._path:
            data = data[key]
        self._token = data

    def headers(self) -> dict:
        if not self._token:
            self._fetch()
        return {self._header_name: self._token, "Content-Type": "application/json"}

    def refresh(self):
        self._token = None
        self._fetch()


class OAuth2ClientCredentials(_BaseAuth):
    """OAuth2 client_credentials grant → Authorization: Bearer {token}.

    Auto-refreshes before the token expires (with a 30-second buffer).

    Args:
        token_url:     Full URL of the OAuth2 token endpoint.
        client_id:     OAuth2 client ID.
        client_secret: OAuth2 client secret.
        scope:         Optional scope string.
        verify_ssl:    Passed to requests.
        timeout:       Seconds before the token request times out.
    """
    def __init__(self, token_url: str, client_id: str, client_secret: str,
                 scope: str = None, verify_ssl: bool = True, timeout: int = 15):
        self._url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = scope
        self._verify = verify_ssl
        self._timeout = timeout
        self._token = None
        self._expires_at = 0.0

    def _fetch(self):
        data = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }
        if self._scope:
            data["scope"] = self._scope
        r = requests.post(self._url, data=data,
                          verify=self._verify, timeout=self._timeout)
        r.raise_for_status()
        resp = r.json()
        self._token = resp["access_token"]
        self._expires_at = time.monotonic() + int(resp.get("expires_in", 3600)) - 30

    def headers(self) -> dict:
        if not self._token or time.monotonic() >= self._expires_at:
            self._fetch()
        return {"Authorization": f"Bearer {self._token}", "Content-Type": "application/json"}

    def refresh(self):
        self._token = None
        self._fetch()


# ---------------------------------------------------------------------------
# Session
# ---------------------------------------------------------------------------

class RestSession:
    """Authenticated HTTP session with transparent 401-retry.

    Wraps requests.request with the chosen auth strategy. On a 401 response
    the auth token is refreshed once and the request is retried — callers
    don't need to handle token expiry themselves.

    Args:
        auth:       Any auth object from this module (or a custom _BaseAuth subclass).
        verify_ssl: Passed to every request.
        timeout:    Default timeout in seconds (can be overridden per call).
    """
    def __init__(self, auth: _BaseAuth, verify_ssl: bool = True, timeout: int = 30):
        self._auth = auth
        self._verify = verify_ssl
        self._timeout = timeout

    def request(self, method: str, url: str,
                raise_on_error: bool = True,
                retry_on_401: bool = True,
                **kwargs) -> requests.Response:
        kwargs.setdefault("verify", self._verify)
        kwargs.setdefault("timeout", self._timeout)
        extra_headers = kwargs.pop("headers", {})

        headers = {**self._auth.headers(), **extra_headers}
        r = requests.request(method, url, headers=headers, **kwargs)

        if r.status_code == 401 and retry_on_401:
            self._auth.refresh()
            headers = {**self._auth.headers(), **extra_headers}
            r = requests.request(method, url, headers=headers, **kwargs)

        if raise_on_error:
            r.raise_for_status()
        return r

    def get(self, url, **kwargs) -> requests.Response:
        return self.request("GET", url, **kwargs)

    def post(self, url, **kwargs) -> requests.Response:
        return self.request("POST", url, **kwargs)

    def put(self, url, **kwargs) -> requests.Response:
        return self.request("PUT", url, **kwargs)

    def patch(self, url, **kwargs) -> requests.Response:
        return self.request("PATCH", url, **kwargs)

    def delete(self, url, **kwargs) -> requests.Response:
        return self.request("DELETE", url, **kwargs)
