from decimal import Decimal

from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Seed catalog with sample categories and products"

    def handle(self, *args, **options):
        categories = [
            {
                "name": "Electronics",
                "slug": "electronics",
                "description": "Devices and gadgets",
            },
            {
                "name": "Fashion",
                "slug": "fashion",
                "description": "Clothing and accessories",
            },
            {
                "name": "Home",
                "slug": "home",
                "description": "Home and kitchen essentials",
            },
        ]

        for data in categories:
            Category.objects.get_or_create(
                name=data["name"],
                defaults={
                    "slug": data["slug"],
                    "description": data["description"],
                },
            )

        products = [
            {
                "category": "Electronics",
                "name": "Wireless Headphones",
                "slug": "wireless-headphones",
                "description": "Noise cancelling",
                "price": Decimal("99.99"),
                "stock": 25,
            },
            {
                "category": "Electronics",
                "name": "Smartphone",
                "slug": "smartphone",
                "description": "128GB storage",
                "price": Decimal("499.00"),
                "stock": 50,
            },
            {
                "category": "Fashion",
                "name": "Classic T-Shirt",
                "slug": "classic-tshirt",
                "description": "100% cotton",
                "price": Decimal("19.99"),
                "stock": 100,
            },
            {
                "category": "Home",
                "name": "Blender",
                "slug": "blender",
                "description": "5-speed blender",
                "price": Decimal("59.99"),
                "stock": 20,
            },
        ]

        for data in products:
            category = Category.objects.get(name=data["category"])
            Product.objects.get_or_create(
                slug=data["slug"],
                defaults={
                    "category": category,
                    "name": data["name"],
                    "description": data["description"],
                    "price": data["price"],
                    "stock": data["stock"],
                    "is_active": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("Catalog seed data created."))
