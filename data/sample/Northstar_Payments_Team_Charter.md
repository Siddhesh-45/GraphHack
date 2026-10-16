# Northstar Systems — Core Payments Team Charter 2026

- **Team Name**: Core Payments
- **Department**: FinTech & Platform Engineering
- **Engineering Director**: Elena Rostova
- **Primary Tech Lead & Service Owner**: Sarah Chen (Staff Backend Engineer)
- **Senior Systems Engineer**: Marcus Vance

## Team Mission
The Core Payments team is responsible for the financial accuracy, availability, and throughput of all monetary flows across Northstar Systems.

## Owned Services
1. **Payment Gateway (`payment-gateway`)**:
   - **Primary Owner**: Sarah Chen
   - **Service Tier**: Tier 1 (Critical)
   - **On-Call Rotation**: PagerDuty primary: Sarah Chen, secondary: Marcus Vance
   - **Repository**: `github.com/northstar/payment-gateway`
2. **Billing Engine (`billing-engine`)**:
   - **Primary Owner**: Marcus Vance
   - **Service Tier**: Tier 2
   - **Repository**: `github.com/northstar/billing-engine`

## Core Dependencies
- Payment Gateway directly calls **Auth Service** (synchronous gRPC) for API token validation.
- Payment Gateway emits async transaction events to **Billing Engine** via Apache Kafka.
