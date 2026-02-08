from rest_framework.test import APITestCase


class TestUser:
    def __init__(self, user_id):
        self.id = user_id

    @property
    def is_authenticated(self):
        return True


class TestPaymentsApi(APITestCase):
    def setUp(self):
        self.client.force_authenticate(user=TestUser("11111111-1111-1111-1111-111111111111"))

    def test_create_payment(self):
        response = self.client.post(
            "/api/payments/payments/",
            {
                "order_id": "11111111-1111-1111-1111-111111111111",
                "amount": "19.99",
                "method": "card",
                "status": "pending",
                "reference": "ref-123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)
