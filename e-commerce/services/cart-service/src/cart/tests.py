from rest_framework.test import APITestCase
import json


class TestCartApi(APITestCase):
    def test_create_cart(self):
        response = self.client.post(
            "/api/cart/carts/",
            {"user_id": "11111111-1111-1111-1111-111111111111"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertIn("id", data)

    def test_add_item_and_total(self):
        cart_response = self.client.post(
            "/api/cart/carts/",
            {"user_id": "11111111-1111-1111-1111-111111111111"},
            format="json",
        )
        cart_data = json.loads(cart_response.content)
        cart_id = cart_data["id"]

        item_response = self.client.post(
            "/api/cart/items/",
            {
                "cart": cart_id,
                "product_id": "22222222-2222-2222-2222-222222222222",
                "product_name": "Test Product",
                "unit_price": "49.99",
                "quantity": 2,
            },
            format="json",
        )
        self.assertEqual(item_response.status_code, 201)

        cart_detail = self.client.get(f"/api/cart/carts/{cart_id}/")
        self.assertEqual(cart_detail.status_code, 200)
        detail_data = json.loads(cart_detail.content)
        self.assertEqual(str(detail_data["total"]), "99.98")
        self.assertEqual(len(detail_data["items"]), 1)
