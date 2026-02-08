#!/usr/bin/env bash
set -euo pipefail

services=(accounts cart catalog orders payments)

declare -A test_labels
test_labels[accounts]="accounts"
test_labels[cart]="cart"
test_labels[catalog]="catalog"
test_labels[orders]="orders"
test_labels[payments]="payments"

for svc in "${services[@]}"; do
  echo "==> Testing ${svc}-service"
  pushd "$(dirname "$0")/../services/${svc}-service" > /dev/null
  poetry run python src/manage.py test "${test_labels[$svc]}"
  popd > /dev/null
  echo ""
done
