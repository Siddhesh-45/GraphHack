# Incident Post-Mortem — INC-102: Auth Token Invalidation Failure

- **Incident ID**: INC-102
- **Severity**: SEV-2 (Elevated Error Rate)
- **Occurred At**: 2026-09-02T08:15:00Z
- **Resolved At**: 2026-09-02T08:45:00Z (Duration: 30 minutes)
- **Lead Incident Resolver**: Alex Rivera (Principal Infrastructure Architect)
- **Affected Services**: Auth Service (`auth-service`), API Gateway (`api-gateway`)

## Summary
A rolling canary deployment of Auth Service version 2.4.0 led to a 12% intermittent 401 Unauthorized rejection rate across incoming client sessions.

## Root Cause
An asymmetric JWT signing key was rotated in the new canary pods, but the public key cache on the existing API Gateway instances had a 1-hour TTL without a forced revocation hook.

## Resolution & Mitigating Actions
1. Alex Rivera triggered an instant cache eviction across all API Gateway pods via the internal management endpoint.
2. Modified the key-rotation protocol to require a 24-hour dual-signature grace period before deprecating prior public keys.
