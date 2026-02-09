# E-Commerce Backend API (Microservices)

This project implements an e-commerce backend split into independent services for accounts, catalog, cart, orders, and payments. Each service exposes a REST API and has its own database schema.

## Services and Base Paths

- Accounts: `/api/accounts/`
- Catalog: `/api/catalog/`
- Cart: `/api/cart/`
- Orders: `/api/orders/`
- Payments: `/api/payments/`

Each service provides:

- `GET /health/`
- Swagger UI: `/api/docs/`
- OpenAPI schema: `/api/schema/`

See `docs/API.md` for full endpoint coverage and examples.

## Current Features (Implemented)

- JWT authentication (accounts) with token refresh.
- User profile management with auto-created profile.
- Product and category CRUD.
- Cart and cart item CRUD with ownership checks.
- Order and order item CRUD with checkout flow.
- Payment and transaction records.
- Service-to-service calls from orders to cart and payments.
- API docs via drf-spectacular.

## Planned / Not Yet Implemented

- Role-based access (admin vs customer).
- Filtering/sorting/pagination for catalog.
- Stripe integration and payment webhooks.
- Production-grade async tasks (Celery/queues).
- Full production hardening (rate limiting, audit logs, etc.).

## Run Locally (Docker Compose)

From repo root:

```bash
docker compose up --build
```

Gateway (Nginx) routes all services on:

- `http://localhost:8080/api/<service>/...`

Direct service ports (if needed):

- Accounts: `http://localhost:8001`
- Cart: `http://localhost:8002`
- Catalog: `http://localhost:8003`
- Orders: `http://localhost:8004`
- Payments: `http://localhost:8005`

## Deployment

### EC2 (Docker Compose)

1. Clone the repo on EC2.
2. Run:

   ```bash
   docker compose up -d --build
   ```
3. Access via the EC2 public IP:

   - Gateway: `http://<EC2_PUBLIC_IP>/api/...` (if Nginx mapped to port 80)

### Railway

- Create one service per microservice.
- Set Root Directory to each service folder:
  - `e-commerce/services/accounts-service` (repeat for others).
- Use Docker build.
- Start command:

  ```bash
  python src/manage.py migrate && python src/manage.py runserver 0.0.0.0:$PORT
  ```

### Render

- Create one web service per microservice.
- Root Directory = each service folder.
- Docker build.
- Set env vars per service (DB, SECRET_KEY, ALLOWED_HOSTS).

## Tech Stack

- Python, Django, Django REST Framework
- drf-spectacular for OpenAPI
- PostgreSQL (local via Docker; managed DB for production)
- Docker + Docker Compose
