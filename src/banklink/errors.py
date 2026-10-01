from __future__ import annotations


class BanklinkError(Exception):
    """Base exception for all Banklink API errors."""

    def __init__(self, status: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(status={self.status}, code={self.code!r}, message={self.message!r})"


class AuthenticationError(BanklinkError):
    """Raised when the API key is missing or invalid (HTTP 401)."""


class InsufficientCreditsError(BanklinkError):
    """Raised when the account has insufficient credits (HTTP 402)."""


class NotFoundError(BanklinkError):
    """Raised when the requested resource does not exist (HTTP 404)."""


class RateLimitError(BanklinkError):
    """Raised when the rate limit has been exceeded (HTTP 429)."""


class OrgNotVerifiedError(BanklinkError):
    """Raised when the organisation must verify its link profile before creating
    live link or access requests (HTTP 403, code ``org_not_verified``)."""


class WebhookSignatureError(BanklinkError):
    """Raised when a webhook's Banklink-Signature header doesn't match its body."""

    def __init__(self, message: str = "Webhook signature verification failed.") -> None:
        super().__init__(400, "webhook_signature_invalid", message)
