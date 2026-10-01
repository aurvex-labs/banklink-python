"""Banklink Python SDK — Official client for the Banklink Open Finance API."""

from __future__ import annotations

from ._client import AsyncClient, SyncClient
from .errors import (
    AuthenticationError,
    BanklinkError,
    InsufficientCreditsError,
    NotFoundError,
    OrgNotVerifiedError,
    RateLimitError,
    WebhookSignatureError,
)
from .webhooks import SIGNATURE_HEADER, construct_event, verify_webhook_signature
from .resources.accounts import AsyncAccounts, Accounts
from .resources.balances import AsyncBalances, Balances
from .resources.link import AsyncLinkResource, LinkResource
from .resources.requests import AsyncRequests, Requests
from .resources.transactions import AsyncTransactions, Transactions
from .types import (
    Account,
    Balance,
    LinkResult,
    HostedRequest,
    ListResponse,
    SyncResult,
    Transaction,
)

_DEFAULT_BASE_URL = "https://api.banklink.co.za/v1"


class Banklink:
    """Synchronous Banklink API client.

    Usage::

        client = Banklink(api_key="bl_live_...")
        accounts = client.accounts.list()

    Or as a context manager::

        with Banklink(api_key="bl_live_...") as client:
            accounts = client.accounts.list()
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ) -> None:
        self._http = SyncClient(api_key, base_url=base_url, timeout=timeout)
        self.accounts = Accounts(self._http)
        self.transactions = Transactions(self._http)
        self.balances = Balances(self._http)
        self.link = LinkResource(self._http)
        self.requests = Requests(self._http)

    def __enter__(self) -> Banklink:
        return self

    def __exit__(self, *_: object) -> None:
        self._http.close()

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._http.close()


class AsyncBanklink:
    """Asynchronous Banklink API client.

    Usage::

        async with AsyncBanklink(api_key="bl_live_...") as client:
            accounts = await client.accounts.list()
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ) -> None:
        self._http = AsyncClient(api_key, base_url=base_url, timeout=timeout)
        self.accounts = AsyncAccounts(self._http)
        self.transactions = AsyncTransactions(self._http)
        self.balances = AsyncBalances(self._http)
        self.link = AsyncLinkResource(self._http)
        self.requests = AsyncRequests(self._http)

    async def __aenter__(self) -> AsyncBanklink:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self._http.close()

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._http.close()


__all__ = [
    # Clients
    "Banklink",
    "AsyncBanklink",
    # Types
    "Account",
    "Transaction",
    "Balance",
    "SyncResult",
    "LinkResult",
    "HostedRequest",
    "ListResponse",
    # Errors
    "BanklinkError",
    "AuthenticationError",
    "InsufficientCreditsError",
    "NotFoundError",
    "OrgNotVerifiedError",
    "RateLimitError",
    "WebhookSignatureError",
    # Webhooks
    "SIGNATURE_HEADER",
    "construct_event",
    "verify_webhook_signature",
]
