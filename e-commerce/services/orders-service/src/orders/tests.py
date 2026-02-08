from unittest.mock import Mock, patch

from rest_framework.test import APITestCase

from .models import Order, OrderItem


class TestUser:
    def __init__(self, user_id):
        self.id = user_id

    @property
    def is_authenticated(self):
        return True


class TestOrdersApi(APITestCase):
    def setUp(self):
        self.client.force_authenticate(user=TestUser("11111111-1111-1111-1111-111111111111"))

    def test_create_order(self):
        response = self.client.post(
            "/api/orders/orders/",
            {
                "user_id": "11111111-1111-1111-1111-111111111111",
                "status": "pending",
                "total_amount": "49.99",
                "shipping_address": "123 Main St",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)

    @patch("orders.views.requests.post")
    @patch("orders.views.requests.get")
    def test_checkout_creates_order_and_items(self, mock_get, mock_post):
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                "items": [
                    {
                        "product_id": "22222222-2222-2222-2222-222222222222",
                        "product_name": "Test Product",
                        "unit_price": "49.99",
                        "quantity": 2,
                    }
                ]
            },
        )
        mock_post.return_value = Mock(ok=True, status_code=201, text="")

        response = self.client.post(
            "/api/orders/orders/checkout/",
            {
                "user_id": "11111111-1111-1111-1111-111111111111",
                "cart_id": "3",
                "shipping_address": "123 Main St",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(response.data["total_amount"], "99.98")


    @patch("orders.views.requests.post")
    @patch("orders.views.requests.get")
    def test_checkout_payment_failure_returns_502(self, mock_get, mock_post):
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                "items": [
                    {
                        "product_id": "22222222-2222-2222-2222-222222222222",
                        "product_name": "Test Product",
                        "unit_price": "49.99",
                        "quantity": 1,
                    }
                ]
            },
        )
        mock_post.return_value = Mock(ok=False, status_code=500, text="payment error")

        response = self.client.post(
            "/api/orders/orders/checkout/",
            {
                "user_id": "11111111-1111-1111-1111-111111111111",
                "cart_id": "3",
                "shipping_address": "123 Main St",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.data["detail"], "Payment creation failed")
