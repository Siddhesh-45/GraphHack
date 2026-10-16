# Northstar Systems — Platform Engineering Team Charter 2026

- **Team Name**: Platform Engineering
- **Department**: Infrastructure & Core Engineering
- **Principal Architect & Team Lead**: Alex Rivera
- **Senior Backend Engineer**: David Kim

## Team Mission
Platform Engineering provides the scalable foundations, ingress gateways, and authentication systems that all Northstar microservices rely on.

## Owned Services
1. **Auth Service (`auth-service`)**:
   - **Primary Owner**: Alex Rivera
   - **Service Tier**: Tier 1 (Critical)
   - **Protocol**: gRPC and HTTPS
   - **Repository**: `github.com/northstar/auth-service`
2. **API Gateway (`api-gateway`)**:
   - **Primary Owner**: Alex Rivera
   - **Service Tier**: Tier 1 (Critical)
   - **Repository**: `github.com/northstar/api-gateway`
3. **Notification Service (`notification-service`)**:
   - **Historical Lead**: David Kim
   - **Interim Support**: Platform Engineering

## Architectural Standards
- All inter-service communications requiring sub-millisecond authentication verification must use gRPC (under ADR-002).
- FalkorDB is deployed as the central context store for organizational intelligence and session memory (ADR-005).
