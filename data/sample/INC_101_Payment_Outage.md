# Incident Post-Mortem — INC-101: Payment Gateway Timeout Outage

- **Incident ID**: INC-101
- **Severity**: SEV-1 (Critical Revenue Impact)
- **Occurred At**: 2026-05-14T14:22:00Z
- **Resolved At**: 2026-05-14T15:05:00Z (Duration: 43 minutes)
- **Lead Incident Resolver**: Sarah Chen (Staff Backend Engineer)
- **Affected Services**: Payment Gateway (`payment-gateway`), Billing Engine (`billing-engine`)

## Summary
Between 14:22 and 15:05 UTC, the Payment Gateway experienced a 98% request failure rate due to database connection pool timeouts following an unexpected 10x traffic spike during a flash merchant promotion.

## Root Cause
The Hikari connection pool was hard-capped at 30 connections per pod, while the inbound async queue allowed up to 1,000 concurrent webhooks, quickly leading to pool starvation.

## Resolution & Mitigating Actions
1. Sarah Chen diagnosed the connection leak and hot-reconfigured the connection pool to max 120 connections with a 1,500ms acquisition timeout.
2. Implemented backpressure rate-limiting at the API Gateway level.
3. Updated runbook and added automated alert triggers when pool utilization exceeds 75%.
