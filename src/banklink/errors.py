from __future__ import annotations


class BankLinkError(Exception):
    """Base exception for all BankLink API errors."""

    def __init__(self, status: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(status={self.status}, code={self.code!r}, message={self.message!r})"


class AuthenticationError(BankLinkError):
    """Raised when the API key is missing or invalid (HTTP 401)."""


class InsufficientCreditsError(BankLinkError):
    """Raised when the account has insufficient credits (HTTP 402)."""


class NotFoundError(BankLinkError):
    """Raised when the requested resource does not exist (HTTP 404)."""


class RateLimitError(BankLinkError):
    """Raised when the rate limit has been exceeded (HTTP 429)."""
