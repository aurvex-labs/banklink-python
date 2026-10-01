# Changelog

## 0.2.0 — 2026-10-01

### Added
- `construct_event()` and `verify_webhook_signature()` to verify the
  `Banklink-Signature` header on webhook deliveries, with replay protection and
  support for both secrets during a rotation. `WebhookSignatureError` is raised
  when verification fails.
- `OrgNotVerifiedError` (HTTP 403, `org_not_verified`), raised when creating a
  live link or access request before your link profile is verified.
- `HostedRequest` gains `kind`, `redirect_url`, `completed_at`, `last_error` and
  `delivery_error`. `requests.create_link()` / `create_access()` accept
  `redirect_url`.

### Fixed
- API errors are parsed from the `{"error": {"code", "message"}}` envelope.
  Previously every error had code `unknown_error` and the raw response body as
  its message.

### Changed
- Live webhook URLs for link and access requests must be https on your verified
  domain (enforced by the API).

## 0.1.0

- Initial release: accounts, transactions, balances, bank linking, hosted link
  and access requests.
