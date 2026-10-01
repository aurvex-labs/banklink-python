from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from ..types import HostedRequest

if TYPE_CHECKING:
    from .._client import AsyncClient, SyncClient


def _parse_request(raw: Dict[str, Any]) -> HostedRequest:
    data = raw["data"]
    return HostedRequest(
        id=data["id"],
        reference=data["reference"],
        token=data["token"],
        url=data["url"],
        status=data["status"],
        bank_id=data.get("bank_id"),
        return_options=data.get("return_options", {}),
        destinations=data.get("destinations", []),
        save_data=data.get("save_data"),
        expires_at=data.get("expires_at"),
        created_at=data["created_at"],
        kind=data.get("kind"),
        redirect_url=data.get("redirect_url"),
        completed_at=data.get("completed_at"),
        last_error=data.get("last_error"),
        delivery_error=data.get("delivery_error"),
    )


class Requests:
    """Synchronous hosted link and access requests."""

    def __init__(self, client: SyncClient) -> None:
        self._client = client

    def create_link(self, **params: Any) -> HostedRequest:
        """Create a persistent link request.

        Takes the API's snake_case fields: ``reference``, ``destinations``, and
        optionally ``name``, ``bank_id``, ``return_options``, ``save_data``,
        ``expires_at`` and ``redirect_url``. Live requests need a verified link
        profile (else :class:`OrgNotVerifiedError`), and webhook and redirect
        URLs must be https on the verified domain.
        """
        return _parse_request(self._client.post("/link-requests", body=params))

    def create_access(self, **params: Any) -> HostedRequest:
        """Create a non-persistent access request."""
        return _parse_request(self._client.post("/access-requests", body=params))


class AsyncRequests:
    """Asynchronous hosted link and access requests."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def create_link(self, **params: Any) -> HostedRequest:
        return _parse_request(await self._client.post("/link-requests", body=params))

    async def create_access(self, **params: Any) -> HostedRequest:
        return _parse_request(await self._client.post("/access-requests", body=params))
