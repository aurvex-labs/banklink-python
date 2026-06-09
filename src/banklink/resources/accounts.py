from __future__ import annotations

from typing import TYPE_CHECKING

from ..types import Account, ListResponse, SyncResult

if TYPE_CHECKING:
    from .._client import AsyncClient, SyncClient


def _parse_account(raw: dict) -> Account:
    return Account(
        id=raw["id"],
        bank=raw["bank"],
        account_number=raw.get("account_number"),
        nickname=raw["nickname"],
        last_synced_at=raw.get("last_synced_at"),
        created_at=raw["created_at"],
    )


class Accounts:
    """Synchronous accounts resource."""

    def __init__(self, client: SyncClient) -> None:
        self._client = client

    def list(self) -> ListResponse[Account]:
        """List all linked bank accounts."""
        raw = self._client.get("/accounts")
        return ListResponse(
            data=[_parse_account(item) for item in raw.get("data", [])],
            cursor=raw.get("cursor"),
        )

    def get(self, account_id: str) -> Account:
        """Retrieve a single bank account by ID."""
        raw = self._client.get(f"/accounts/{account_id}")
        return _parse_account(raw)

    def sync(self, account_id: str) -> SyncResult:
        """Trigger an on-demand sync for the given account."""
        raw = self._client.post(f"/accounts/{account_id}/sync")
        return SyncResult(
            synced=raw["synced"],
            skipped=raw["skipped"],
        )


class AsyncAccounts:
    """Asynchronous accounts resource."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(self) -> ListResponse[Account]:
        """List all linked bank accounts."""
        raw = await self._client.get("/accounts")
        return ListResponse(
            data=[_parse_account(item) for item in raw.get("data", [])],
            cursor=raw.get("cursor"),
        )

    async def get(self, account_id: str) -> Account:
        """Retrieve a single bank account by ID."""
        raw = await self._client.get(f"/accounts/{account_id}")
        return _parse_account(raw)

    async def sync(self, account_id: str) -> SyncResult:
        """Trigger an on-demand sync for the given account."""
        raw = await self._client.post(f"/accounts/{account_id}/sync")
        return SyncResult(
            synced=raw["synced"],
            skipped=raw["skipped"],
        )
