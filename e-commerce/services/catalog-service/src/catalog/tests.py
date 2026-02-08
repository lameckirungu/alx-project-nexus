from decimal import Decimal

from rest_framework.test import APITestCase

from .models import Category, Product


class TestCatalogApi(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
            description="Devices and gadgets",
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Wireless Headphones",
            slug="wireless-headphones",
            description="Noise cancelling",
            price=Decimal("99.99"),
            stock=10,
            is_active=True,
        )

    def test_list_categories(self):
        response = self.client.get("/api/catalog/categories/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Electronics")

    def test_list_products(self):
        response = self.client.get("/api/catalog/products/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Wireless Headphones")

    def test_update_product_stock(self):
        response = self.client.patch(
            f"/api/catalog/products/{self.product.pk}/",
            {"stock": 5},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["stock"], 5)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)
