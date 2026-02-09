# API Documentation

## Access After Deployment (EC2)

When you deploy to a server, you no longer use `localhost`. You use the server's public IP or domain.

If you run Nginx gateway (recommended):

- Base URL: `http://<EC2_PUBLIC_IP>`
- Example: `http://<EC2_PUBLIC_IP>/api/catalog/health/`

Deployed for evaluation:

- Base URL: `http://54.161.28.134/`

If you expose each service port directly (no gateway):

- Accounts: `http://<EC2_PUBLIC_IP>:8001`
- Cart: `http://<EC2_PUBLIC_IP>:8002`
- Catalog: `http://<EC2_PUBLIC_IP>:8003`
- Orders: `http://<EC2_PUBLIC_IP>:8004`
- Payments: `http://<EC2_PUBLIC_IP>:8005`

Security group rules must allow inbound traffic on the ports you use. If you use the gateway, open port `80` (and optionally `443`). If you expose services directly, open `8001-8005`.

## Overview
This project is a microservices-based e-commerce backend. Each service exposes a REST API and is deployed independently.

Local base URLs:

- Accounts: `http://localhost:8001`
- Cart: `http://localhost:8002`
- Catalog: `http://localhost:8003`
- Orders: `http://localhost:8004`
- Payments: `http://localhost:8005`

Swagger docs per service:

- `GET /api/docs/`
- `GET /api/schema/`

## Authentication

- JWT authentication via `djangorestframework-simplejwt`.
- Use `Authorization: Bearer <jwt>` for protected endpoints.

Example login:

```http
POST /api/accounts/auth/login/
Content-Type: application/json

{
  "username": "demo",
  "password": "Passw0rd!"
}
```

Response:
```json
{
  "access": "<jwt>",
  "refresh": "<jwt>"
}
```

## Accounts Service

Base path: `/api/accounts/`

Endpoints:

- `GET /health/`
- `POST /register/`
- `POST /auth/login/`
- `POST /auth/refresh/`
- `GET /auth/me/`
- `GET /users/`
- `GET /users/{id}/`
- `GET /profiles/`
- `GET /profiles/{id}/`
- `PATCH /profiles/{id}/`
- `PUT /profiles/{id}/`
- `DELETE /profiles/{id}/`

Register example:

```http
POST /api/accounts/register/
Content-Type: application/json

{
  "username": "demo",
  "email": "demo@example.com",
  "password": "Passw0rd!",
  "first_name": "Demo",
  "last_name": "User"
}
```

## Catalog Service

Base path: `/api/catalog/`

Endpoints:

- `GET /health/`
- `GET /categories/`
- `POST /categories/`
- `GET /categories/{id}/`
- `PUT /categories/{id}/`
- `PATCH /categories/{id}/`
- `DELETE /categories/{id}/`
- `GET /products/`
- `POST /products/`
- `GET /products/{id}/`
- `PUT /products/{id}/`
- `PATCH /products/{id}/`
- `DELETE /products/{id}/`

## Cart Service

Base path: `/api/cart/`

Endpoints:

- `GET /health/`
- `GET /carts/`
- `POST /carts/`
- `GET /carts/{id}/`
- `PATCH /carts/{id}/`
- `DELETE /carts/{id}/`
- `GET /items/`
- `POST /items/`
- `GET /items/{id}/`
- `PATCH /items/{id}/`
- `DELETE /items/{id}/`

Example add item:

```http
POST /api/cart/items/
Authorization: Bearer <jwt>
Content-Type: application/json

{
  "cart": "<cart_id>",
  "product_id": "<product_uuid>",
  "product_name": "Test Product",
  "unit_price": "49.99",
  "quantity": 2
}
```

## Orders Service

Base path: `/api/orders/`

Endpoints:

- `GET /health/`
- `GET /orders/`
- `POST /orders/`
- `GET /orders/{id}/`
- `PATCH /orders/{id}/`
- `DELETE /orders/{id}/`
- `POST /orders/checkout/`
- `GET /items/`
- `POST /items/`
- `GET /items/{id}/`

Checkout example:

```http
POST /api/orders/orders/checkout/
Authorization: Bearer <jwt>
Content-Type: application/json

{
  "cart_id": "<cart_id>",
  "shipping_address": "123 Main St"
}
```

## Payments Service

Base path: `/api/payments/`

Endpoints:

- `GET /health/`
- `GET /payments/`
- `POST /payments/`
- `GET /payments/{id}/`
- `POST /payments/create_for_order/`
- `GET /transactions/`
- `POST /transactions/`

Example create payment for order:

```http
POST /api/payments/payments/create_for_order/
Authorization: Bearer <jwt>
Content-Type: application/json

{
  "order_id": "<order_id>",
  "amount": 100.00,
  "method": "card"
}
```

## Example Usage (Postman / Frontend)

1. Register a user via Accounts service.
2. Login to get a JWT.
3. Use `Authorization: Bearer <jwt>` for Cart, Orders, and Payments.
4. Use Catalog endpoints without auth (current configuration).

## Best Practices Applied

- RESTful resource-oriented endpoints and standard HTTP verbs.
- JWT authentication with short-lived access tokens.
- Owner-based authorization checks in cart/orders/payments.
- Serializer validation for request data.
- Clear service boundaries by domain.
- Health check endpoints for monitoring.
- OpenAPI docs via drf-spectacular.
