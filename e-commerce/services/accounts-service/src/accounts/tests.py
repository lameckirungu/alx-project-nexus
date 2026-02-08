from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class TestAccountsApi(APITestCase):
	def test_register_user(self):
		response = self.client.post(
			"/api/accounts/register/",
			{
				"username": "demo",
				"email": "demo@example.com",
				"password": "Passw0rd!",
				"first_name": "Demo",
				"last_name": "User",
			},
			format="json",
		)
		self.assertEqual(response.status_code, 201)
		self.assertTrue(User.objects.filter(username="demo").exists())
