from __future__ import annotations

from typing import TYPE_CHECKING

from ..types import Balance

if TYPE_CHECKING:
    from .._client import AsyncClient, SyncClient


class Balances:
    """Synchronous balances resource."""

    def __init__(self, client: SyncClient) -> None:
        self._client = client

    def get(self, account_id: str) -> Balance:
        """Retrieve the current balance for the given account."""
        raw = self._client.get(f"/accounts/{account_id}/balance")
        return Balance(
            account_id=raw["account_id"],
            balance=float(raw["balance"]) if raw.get("balance") is not None else None,
            currency=raw["currency"],
            last_synced_at=raw.get("last_synced_at"),
        )


class AsyncBalances:
    """Asynchronous balances resource."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def get(self, account_id: str) -> Balance:
        """Retrieve the current balance for the given account."""
        raw = await self._client.get(f"/accounts/{account_id}/balance")
        return Balance(
            account_id=raw["account_id"],
            balance=float(raw["balance"]) if raw.get("balance") is not None else None,
            currency=raw["currency"],
            last_synced_at=raw.get("last_synced_at"),
        )
