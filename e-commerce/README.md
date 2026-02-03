# E-Commerce Backend API

Many SMEs need a secure, scalable backend to manage products, users, carts, and payments without building everything from scratch.
This project aims to build a production-ready e-commerce backend API that supports core shipping workflows and can be consumed by any frontend (web or mobile).

## Project Objectives

- Build a RESTful backend API for an e-commerce platform
- Implement secure authentication and authorization
- Support product discovery, cart management, and payments
- Deploy the API using AWS serverless services
- Provide clear API documentation for frontend integration

## Core Features

### 1. Authentication and Users

- User registration and login
- JWT-based authentication
- Role-based access (admin vs customer)

_**Endpoints**_

- `POST /auth/register`
- `POST /auth/login`
- `GET  /auth/profile`

### 2. Product & Category Management

- CRUD operations for products
- Product categorization
- Filtering, sorting, and pagination
- Admin-only product management

_**Endpoints**_

```http
GET /products
POST /products # admin
GET /products/{id}
PUT /products/{id} # admin
DELETE /products/{id} # admin
```

### 3. Cart Management

- Add products to cart
- Remove products from cart
- View cart contents
- Update product quantities

_**Endpoints**_

```http
POST /cart/add
POST /cart/remove
GET /cart
```

### 4. Orders & Payments
- Checkout process
- Payment processing using stripe
- Order creation after successful payment
- Order history per user

_**Endpoints**_

```http
POST /checkout
GET /orders
GET /orders/{id}
```

### 5. API Documentation

- Swagger documentation
- Publicly accessible API docs
- Example requests and responses

## Technologies & Tools

_Backend_

- Python
- Django + Django REST Framework
- JWT Authentication

_Database_

- PostgreSQL (AWS RDS)
- Indexed fields for performance

_Cloud & Deployment_

- AWS Lambda
- AWS API Gateway
- AWS IAM
- AWS CloudWatch (logs)

_Payments_

- Stripe API

_Testing_

- Postman

_Version Control_

- Git & GitHub