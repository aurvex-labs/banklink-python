from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from .errors import (
    OrgNotVerifiedError,
    AuthenticationError,
    BanklinkError,
    InsufficientCreditsError,
    NotFoundError,
    RateLimitError,
)

_DEFAULT_BASE_URL = "https://api.banklink.co.za/v1"
_USER_AGENT = "banklink-python/0.2.0"

_ERROR_MAP = {
    401: AuthenticationError,
    402: InsufficientCreditsError,
    404: NotFoundError,
    429: RateLimitError,
}


def _raise_for_status(response: httpx.Response) -> None:
    if response.is_success:
        return
    status = response.status_code
    try:
        payload = response.json()
        # v1 errors are {"error": {"code", "message"}}; tolerate {"error": "..."} too.
        error = payload.get("error")
        if isinstance(error, dict):
            code = error.get("code", "unknown_error")
            message = error.get("message", response.text)
        else:
            code = payload.get("code", "unknown_error")
            message = error if isinstance(error, str) else payload.get("message", response.text)
    except Exception:
        code = "unknown_error"
        message = response.text

    if code == "org_not_verified":
        raise OrgNotVerifiedError(status, code, message)
    exc_class = _ERROR_MAP.get(status, BanklinkError)
    raise exc_class(status, code, message)


class SyncClient:
    """Synchronous HTTP client for the Banklink API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._http = httpx.Client(
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": _USER_AGENT,
            },
            timeout=timeout,
        )

    def request(
        self,
        method: str,
        path: str,
        body: Optional[Dict[str, Any]] = None,
    ) -> Any:
        url = f"{self._base_url}{path}"
        response = self._http.request(method, url, json=body)
        _raise_for_status(response)
        return response.json()

    def get(self, path: str) -> Any:
        return self.request("GET", path)

    def post(self, path: str, body: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("POST", path, body=body)

    def close(self) -> None:
        self._http.close()


class AsyncClient:
    """Asynchronous HTTP client for the Banklink API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._http = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": _USER_AGENT,
            },
            timeout=timeout,
        )

    async def request(
        self,
        method: str,
        path: str,
        body: Optional[Dict[str, Any]] = None,
    ) -> Any:
        url = f"{self._base_url}{path}"
        response = await self._http.request(method, url, json=body)
        _raise_for_status(response)
        return response.json()

    async def get(self, path: str) -> Any:
        return await self.request("GET", path)

    async def post(self, path: str, body: Optional[Dict[str, Any]] = None) -> Any:
        return await self.request("POST", path, body=body)

    async def close(self) -> None:
        await self._http.aclose()
