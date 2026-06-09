from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator, Iterator, Optional

from ..types import ListResponse, Transaction

if TYPE_CHECKING:
    from .._client import AsyncClient, SyncClient


def _parse_transaction(raw: dict) -> Transaction:
    return Transaction(
        id=raw["id"],
        account_id=raw["account_id"],
        external_id=raw["external_id"],
        date=raw["date"],
        description=raw["description"],
        amount=float(raw["amount"]),
        currency=raw["currency"],
        direction=raw["direction"],
        balance=float(raw["balance"]) if raw.get("balance") is not None else None,
        reference=raw.get("reference"),
        created_at=raw["created_at"],
    )


def _build_path(
    account_id: str,
    limit: Optional[int],
    cursor: Optional[str],
) -> str:
    path = f"/accounts/{account_id}/transactions"
    params: list[str] = []
    if limit is not None:
        params.append(f"limit={limit}")
    if cursor is not None:
        params.append(f"cursor={cursor}")
    if params:
        path = f"{path}?{'&'.join(params)}"
    return path


class Transactions:
    """Synchronous transactions resource."""

    def __init__(self, client: SyncClient) -> None:
        self._client = client

    def list(
        self,
        account_id: str,
        *,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> ListResponse[Transaction]:
        """Fetch a single page of transactions for the given account."""
        path = _build_path(account_id, limit, cursor)
        raw = self._client.get(path)
        return ListResponse(
            data=[_parse_transaction(item) for item in raw.get("data", [])],
            cursor=raw.get("cursor"),
        )

    def list_auto_paginate(
        self,
        account_id: str,
        *,
        limit: Optional[int] = None,
    ) -> Iterator[Transaction]:
        """Yield all transactions across all pages automatically."""
        cursor: Optional[str] = None
        while True:
            page = self.list(account_id, limit=limit, cursor=cursor)
            yield from page.data
            if page.cursor is None:
                break
            cursor = page.cursor


class AsyncTransactions:
    """Asynchronous transactions resource."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(
        self,
        account_id: str,
        *,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> ListResponse[Transaction]:
        """Fetch a single page of transactions for the given account."""
        path = _build_path(account_id, limit, cursor)
        raw = await self._client.get(path)
        return ListResponse(
            data=[_parse_transaction(item) for item in raw.get("data", [])],
            cursor=raw.get("cursor"),
        )

    async def list_auto_paginate(
        self,
        account_id: str,
        *,
        limit: Optional[int] = None,
    ) -> AsyncIterator[Transaction]:
        """Yield all transactions across all pages automatically."""
        cursor: Optional[str] = None
        while True:
            page = await self.list(account_id, limit=limit, cursor=cursor)
            for txn in page.data:
                yield txn
            if page.cursor is None:
                break
            cursor = page.cursor
