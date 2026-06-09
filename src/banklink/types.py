from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Account:
    id: str
    bank: str
    account_number: Optional[str]
    nickname: str
    last_synced_at: Optional[str]
    created_at: str


@dataclass(frozen=True)
class Transaction:
    id: str
    account_id: str
    external_id: str
    date: str
    description: str
    amount: float
    currency: str
    direction: str
    balance: Optional[float]
    reference: Optional[str]
    created_at: str


@dataclass(frozen=True)
class Balance:
    account_id: str
    balance: Optional[float]
    currency: str
    last_synced_at: Optional[str]


@dataclass(frozen=True)
class SyncResult:
    synced: int
    skipped: int


@dataclass(frozen=True)
class LinkResult:
    type: str
    profile_id: Optional[str] = None
    account_number: Optional[str] = None
    session_token: Optional[str] = None
    message: Optional[str] = None


@dataclass(frozen=True)
class ListResponse(Generic[T]):
    data: List[T]
    cursor: Optional[str]
