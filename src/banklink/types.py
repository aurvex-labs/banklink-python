from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Generic, List, Optional, TypeVar

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
class HostedRequest:
    id: str
    reference: str
    token: str
    url: str
    status: str
    bank_id: Optional[str]
    return_options: Dict[str, str]
    destinations: List[Dict[str, Any]]
    save_data: Optional[bool]
    expires_at: Optional[str]
    created_at: str
    kind: Optional[str] = None
    """``"link"`` keeps an encrypted login for later fetches; ``"access"`` fetches once."""
    redirect_url: Optional[str] = None
    completed_at: Optional[str] = None
    last_error: Optional[str] = None
    delivery_error: Optional[str] = None
    """Set when the bank fetch succeeded but a webhook/email delivery failed."""


@dataclass(frozen=True)
class ListResponse(Generic[T]):
    data: List[T]
    cursor: Optional[str]
