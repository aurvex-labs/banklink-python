from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

from ..types import LinkResult

if TYPE_CHECKING:
    from .._client import AsyncClient, SyncClient


def _parse_link_result(raw: dict) -> LinkResult:
    return LinkResult(
        type=raw["type"],
        profile_id=raw.get("profile_id"),
        account_number=raw.get("account_number"),
        session_token=raw.get("session_token"),
        message=raw.get("message"),
    )


class LinkResource:
    """Synchronous link resource for connecting bank accounts."""

    def __init__(self, client: SyncClient) -> None:
        self._client = client

    def create(
        self,
        *,
        bank_id: str,
        credentials: Dict[str, str],
        nickname: Optional[str] = None,
    ) -> LinkResult:
        """Initiate a bank account link flow."""
        body: Dict[str, object] = {
            "bankId": bank_id,
            "credentials": credentials,
        }
        if nickname is not None:
            body["nickname"] = nickname
        raw = self._client.post("/link", body=body)
        return _parse_link_result(raw)

    def submit_otp(self, *, session_token: str, otp: str) -> LinkResult:
        """Submit an OTP to complete a multi-step link flow."""
        raw = self._client.post(
            "/link/otp",
            body={"session_token": session_token, "otp": otp},
        )
        return _parse_link_result(raw)


class AsyncLinkResource:
    """Asynchronous link resource for connecting bank accounts."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def create(
        self,
        *,
        bank_id: str,
        credentials: Dict[str, str],
        nickname: Optional[str] = None,
    ) -> LinkResult:
        """Initiate a bank account link flow."""
        body: Dict[str, object] = {
            "bankId": bank_id,
            "credentials": credentials,
        }
        if nickname is not None:
            body["nickname"] = nickname
        raw = await self._client.post("/link", body=body)
        return _parse_link_result(raw)

    async def submit_otp(self, *, session_token: str, otp: str) -> LinkResult:
        """Submit an OTP to complete a multi-step link flow."""
        raw = await self._client.post(
            "/link/otp",
            body={"session_token": session_token, "otp": otp},
        )
        return _parse_link_result(raw)
