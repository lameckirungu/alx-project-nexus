#!/bin/bash
# Script to run all microservices

set -e

echo "🚀 Starting all microservices..."
echo ""

# Port assignments
ACCOUNTS_PORT=8001
CART_PORT=8002
CATALOG_PORT=8003
ORDERS_PORT=8004
PAYMENTS_PORT=8005

# Function to run a service
run_service() {
    local service=$1
    local port=$2
    
    echo "Starting $service on port $port..."
    cd "services/${service}-service" || exit 1
    poetry run python src/manage.py runserver $port &
    cd - > /dev/null
}

# Clean up background processes on exit
trap 'echo ""; echo "🛑 Stopping all services..."; kill $(jobs -p) 2>/dev/null; exit' INT TERM

# Start all services
run_service "accounts" $ACCOUNTS_PORT
run_service "cart" $CART_PORT
run_service "catalog" $CATALOG_PORT
run_service "orders" $ORDERS_PORT
run_service "payments" $PAYMENTS_PORT

echo ""
echo "✅ All services started!"
echo ""
echo "📍 Service URLs:"
echo "   Accounts:  http://localhost:$ACCOUNTS_PORT"
echo "   Cart:      http://localhost:$CART_PORT"
echo "   Catalog:   http://localhost:$CATALOG_PORT"
echo "   Orders:    http://localhost:$ORDERS_PORT"
echo "   Payments:  http://localhost:$PAYMENTS_PORT"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for all background processes
wait
