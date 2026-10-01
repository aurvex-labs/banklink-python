"""Verify Banklink webhook signatures.

Every webhook delivery carries ``Banklink-Signature: t=<unix>,v1=<hex>``, an
HMAC-SHA256 of ``f"{t}.{raw_body}"`` keyed with your organisation's webhook
secret (Settings → Webhook signing secret in the dashboard).
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import time
from typing import Any, Dict, Optional, Union

from .errors import WebhookSignatureError

SIGNATURE_HEADER = "Banklink-Signature"
DEFAULT_TOLERANCE_SECONDS = 300
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def verify_webhook_signature(
    payload: Union[str, bytes],
    header: Optional[str],
    secret: str,
    tolerance: int = DEFAULT_TOLERANCE_SECONDS,
) -> bool:
    """Return True if ``header`` is a valid, recent signature of ``payload``.

    Pass the raw request body exactly as received, not re-serialised JSON.
    During a secret rotation the header carries two ``v1`` values; either
    matching is enough.
    """
    if not header:
        return False
    body = payload.decode("utf-8") if isinstance(payload, bytes) else payload
    parts = [p.strip().split("=", 1) for p in header.split(",")]
    pairs = [(p[0], p[1]) for p in parts if len(p) == 2]
    try:
        timestamp = int(next(v for k, v in pairs if k == "t"))
    except (StopIteration, ValueError):
        return False
    if abs(int(time.time()) - timestamp) > tolerance:
        return False
    expected = hmac.new(secret.encode(), f"{timestamp}.{body}".encode(), hashlib.sha256).hexdigest()
    return any(k == "v1" and _HEX64.match(v) and hmac.compare_digest(expected, v) for k, v in pairs)


def construct_event(
    payload: Union[str, bytes],
    header: Optional[str],
    secret: str,
    tolerance: int = DEFAULT_TOLERANCE_SECONDS,
) -> Dict[str, Any]:
    """Verify a webhook and return its parsed JSON body.

    Raises :class:`WebhookSignatureError` if the signature doesn't match.

    Example (Flask)::

        event = construct_event(request.get_data(), request.headers.get("Banklink-Signature"), SECRET)
        if event["event"] == "link_request.completed":
            ...
    """
    if not verify_webhook_signature(payload, header, secret, tolerance):
        raise WebhookSignatureError()
    body = payload.decode("utf-8") if isinstance(payload, bytes) else payload
    return json.loads(body)
