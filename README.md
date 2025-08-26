## RESTful Payment Gateway API for SME
### Project Overview and Philosophy
This project aims to provide small and medium enterprises (SMEs) with a simple, secure, and scalable backend API to accept payments from customers. The philosophy centers on delivering a minimal yet robust payment processing system that minimizes friction for SMEs to integrate digital payment acceptance without requiring complex user authentication or frontend dependencies.

Payments are essential for modern commerce, yet many SMEs struggle with integrating payment gateways securely and efficiently. This project responds to that challenge by offering a RESTful API focusing on:

Minimal required customer information (name, email, phone, amount, location).

Clear versioning of API endpoints to future-proof integration and allow smooth evolution.

No user authentication, simplifying access while emphasizing idempotent, secure payment flow where appropriate.

Automated testing and deployment pipelines to ensure reliability and rapid iteration.

## Problem Addressed
* SMEs increasingly need to accept online payments but face challenges including:

--Complexity of payment gateway integrations with diverse APIs.

Managing sensitive customer financial data requires compliance and security.

Providing clear, real-time feedback about payment status.

Keeping the backend maintainable and extensible over time.

Ensuring that changes to API endpoints do not disrupt existing clients (hence versioning).

Automating tests and deployment to maintain quality and reduce manual overhead.

This API seeks to solve these through a targeted design anchored on Django and third-party payment integration with Paystack, backed by PostgreSQL database management and solid CI/CD practices.

Technologies and Tools
Django & Django REST Framework: Web framework and REST API toolkit powering secure, maintainable backend logic.

Paystack Payment Gateway: Robust, trusted payment provider offering APIs for seamless transaction processing.

PostgreSQL: Reliable, scalable relational database for persisting payment data and transaction records.

Unit Testing: Using Django's testing framework to verify core features like payment initiation, status retrieval, and edge cases.

GitHub Actions: Automates testing and deployment workflows, ensuring code quality and enabling continuous delivery.

API Versioning: Implemented with URL path versioning (/api/v1/) to allow backward-compatible API evolution.

API Endpoints
POST /api/v1/payments/
Initiates a payment with customer details and amount. Returns payment reference and status.

GET /api/v1/payments/{id}/
Retrieves status and details of a specific payment transaction by its ID.

Example response for GET payment status:
