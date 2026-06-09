"""BankLink Python SDK — Official client for the BankLink Open Finance API."""

from __future__ import annotations

from ._client import AsyncClient, SyncClient
from .errors import (
    AuthenticationError,
    BankLinkError,
    InsufficientCreditsError,
    NotFoundError,
    RateLimitError,
)
from .resources.accounts import AsyncAccounts, Accounts
from .resources.balances import AsyncBalances, Balances
from .resources.link import AsyncLinkResource, LinkResource
from .resources.transactions import AsyncTransactions, Transactions
from .types import (
    Account,
    Balance,
    LinkResult,
    ListResponse,
    SyncResult,
    Transaction,
)

_DEFAULT_BASE_URL = "https://api.banklink.co.za/v1"


class BankLink:
    """Synchronous BankLink API client.

    Usage::

        client = BankLink(api_key="bl_live_...")
        accounts = client.accounts.list()

    Or as a context manager::

        with BankLink(api_key="bl_live_...") as client:
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

    def __enter__(self) -> BankLink:
        return self

    def __exit__(self, *_: object) -> None:
        self._http.close()

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._http.close()


class AsyncBankLink:
    """Asynchronous BankLink API client.

    Usage::

        async with AsyncBankLink(api_key="bl_live_...") as client:
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

    async def __aenter__(self) -> AsyncBankLink:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self._http.close()

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._http.close()


__all__ = [
    # Clients
    "BankLink",
    "AsyncBankLink",
    # Types
    "Account",
    "Transaction",
    "Balance",
    "SyncResult",
    "LinkResult",
    "ListResponse",
    # Errors
    "BankLinkError",
    "AuthenticationError",
    "InsufficientCreditsError",
    "NotFoundError",
    "RateLimitError",
]
