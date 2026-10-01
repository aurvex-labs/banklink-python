# Banklink Python SDK

Official Python SDK for the [Banklink](https://banklink.co.za) Open Finance API. Link South African bank accounts, ingest transactions, and deliver them anywhere.

## Install

```bash
pip install banklink
```

## Quick Start

```python
from banklink import Banklink

client = Banklink(api_key="bl_live_...")

# List all linked accounts
accounts = client.accounts.list()
for account in accounts.data:
    print(account.id, account.bank, account.account_number)

# Fetch a single page of transactions
page = client.transactions.list("acc_123", limit=50)
for txn in page.data:
    print(txn.date, txn.description, txn.amount, txn.direction)

# Auto-paginate through all transactions
for txn in client.transactions.list_auto_paginate("acc_123"):
    print(txn.date, txn.amount)

# Get account balance
balance = client.balances.get("acc_123")
print(balance.balance, balance.currency)

# Trigger an on-demand sync
result = client.accounts.sync("acc_123")
print(f"Synced {result.synced} transactions, skipped {result.skipped}")
```

## Async Support

```python
import asyncio
from banklink import AsyncBanklink

async def main():
    async with AsyncBanklink(api_key="bl_live_...") as client:
        accounts = await client.accounts.list()
        for account in accounts.data:
            print(account.id, account.bank)

        # Async auto-pagination
        async for txn in client.transactions.list_auto_paginate("acc_123"):
            print(txn.date, txn.amount)

asyncio.run(main())
```

## Bank Linking

```python
from banklink import Banklink

client = Banklink(api_key="bl_live_...")

# Initiate a link flow
result = client.link.create(
    bank_id="fnb",
    credentials={"username": "your_username", "password": "your_password"},
    nickname="My FNB Account",
)

if result.type == "otp_required":
    # Submit OTP if required
    result = client.link.submit_otp(
        session_token=result.session_token,
        otp="123456",
    )

print("Linked:", result.profile_id, result.account_number)
```

## Hosted request links

Live requests need a verified link profile: see
[Verify your organisation](https://banklink.co.za/resources/verify-organisation-link-requests).
Until then they raise `OrgNotVerifiedError`; test keys (`sk_test_`) work straight away.
Live webhook and redirect URLs must be https on your verified domain.

```python
link_request = client.requests.create_link(
    reference="customer-4821",
    bank_id="fnb",
    return_options={"dateFrom": "2026-08-01", "dateTo": "2026-08-31"},
    destinations=[{"type": "webhook", "url": "https://example.co.za/banklink"}],
    save_data=True,
    # Optional. Banklink appends banklink_status and banklink_reference.
    redirect_url="https://example.co.za/onboarding/bank-done",
)

access_request = client.requests.create_access(
    reference="affordability-check-774",
    destinations=[{"type": "webhook", "url": "https://example.co.za/banklink"}],
)

print(link_request.url, access_request.url)
```

## Verifying webhooks

Every webhook carries a `Banklink-Signature` header signed with your webhook
signing secret (dashboard → Settings → Webhook signing). Verify it against the
**raw** request body before trusting the payload:

```python
from banklink import construct_event, WebhookSignatureError

@app.post("/banklink")
def banklink_webhook():
    try:
        event = construct_event(request.get_data(), request.headers.get("Banklink-Signature"), WEBHOOK_SECRET)
    except WebhookSignatureError:
        return "", 400
    if event["event"] == "access_request.completed":
        ...  # event["reference"], event["transactions"]
    return "", 200
```

`verify_webhook_signature(raw_body, header, secret, tolerance=300)` returns a
bool if you'd rather handle it yourself. Signatures older than the tolerance are
rejected, and either secret is accepted during the 24 hours after a rotation.
Use the `Banklink-Delivery` header to ignore duplicate deliveries.

## Error Handling

```python
from banklink import Banklink, AuthenticationError, NotFoundError, OrgNotVerifiedError, RateLimitError, BanklinkError

client = Banklink(api_key="bl_live_...")

try:
    account = client.accounts.get("acc_does_not_exist")
except AuthenticationError:
    print("Invalid or missing API key")
except NotFoundError:
    print("Account not found")
except RateLimitError:
    print("Rate limit exceeded — back off and retry")
except OrgNotVerifiedError:
    print("Verify your link profile before creating live link requests")
except BanklinkError as e:
    print(f"API error {e.status}: [{e.code}] {e.message}")
```

## Configuration

```python
from banklink import Banklink

client = Banklink(
    api_key="bl_live_...",
    base_url="https://api.banklink.co.za/v1",  # default
    timeout=30.0,                               # seconds, default 30
)
```

Use the context manager to ensure connections are closed:

```python
with Banklink(api_key="bl_live_...") as client:
    accounts = client.accounts.list()
```

## Requirements

- Python 3.9+
- [httpx](https://www.python-httpx.org/) >= 0.24 (installed automatically)

## License

MIT — Copyright (c) 2026 Aurvex Labs
