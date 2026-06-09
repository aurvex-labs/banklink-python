# BankLink Python SDK

Official Python SDK for the [BankLink](https://banklink.co.za) Open Finance API. Link South African bank accounts, ingest transactions, and deliver them anywhere.

## Install

```bash
pip install banklink
```

## Quick Start

```python
from banklink import BankLink

client = BankLink(api_key="bl_live_...")

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
from banklink import AsyncBankLink

async def main():
    async with AsyncBankLink(api_key="bl_live_...") as client:
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
from banklink import BankLink

client = BankLink(api_key="bl_live_...")

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

## Error Handling

```python
from banklink import BankLink, AuthenticationError, NotFoundError, RateLimitError, BankLinkError

client = BankLink(api_key="bl_live_...")

try:
    account = client.accounts.get("acc_does_not_exist")
except AuthenticationError:
    print("Invalid or missing API key")
except NotFoundError:
    print("Account not found")
except RateLimitError:
    print("Rate limit exceeded — back off and retry")
except BankLinkError as e:
    print(f"API error {e.status}: [{e.code}] {e.message}")
```

## Configuration

```python
from banklink import BankLink

client = BankLink(
    api_key="bl_live_...",
    base_url="https://api.banklink.co.za/v1",  # default
    timeout=30.0,                               # seconds, default 30
)
```

Use the context manager to ensure connections are closed:

```python
with BankLink(api_key="bl_live_...") as client:
    accounts = client.accounts.list()
```

## Requirements

- Python 3.9+
- [httpx](https://www.python-httpx.org/) >= 0.24 (installed automatically)

## License

MIT — Copyright (c) 2026 Aurvex Labs
