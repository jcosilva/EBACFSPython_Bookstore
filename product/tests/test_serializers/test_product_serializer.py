from rest_framework.exceptions import ValidationError
from django.test import TestCase
from product.serializers import ProductSerializer
from product.factories import CategoryFactory, ProductFactory
from product.models import Product


class TestProductSerializer(TestCase):

    def setUp(self):
        self.category1 = CategoryFactory(title="Eletrônicos")
        self.category2 = CategoryFactory(title="Acessórios")
        self.product = ProductFactory(
            title="Headset Gamer",
            description="Headset com som surround",
            price=250.00,
            active=True,
        )
        self.product.category.add(self.category1, self.category2)

    def test_serializer_valid_data(self):
        serializer = ProductSerializer(instance=self.product)

        expected_data = {
            "id": self.product.id,
            "title": self.product.title,
            "description": self.product.description,
            "price": self.product.price,
            "active": self.product.active,
            "category": [
                {
                    "title": self.category1.title,
                    "slug": self.category1.slug,
                    "description": self.category1.description,
                    "active": self.category1.active,
                },
                {
                    "title": self.category2.title,
                    "slug": self.category2.slug,
                    "description": self.category2.description,
                    "active": self.category2.active,
                },
            ],
            "categories_id": [],
        }

        self.assertEqual(serializer.data, expected_data)

    def test_serializer_valid_data(self):
        serializer = ProductSerializer(instance=self.product)

        expected_data = {
            "id": self.product.id,
            "title": self.product.title,
            "description": self.product.description,
            "price": float(self.product.price),
            "active": self.product.active,
            "category": [
                {
                    "title": self.category1.title,
                    "slug": self.category1.slug,
                    "description": self.category1.description,
                    "active": self.category1.active,
                },
                {
                    "title": self.category2.title,
                    "slug": self.category2.slug,
                    "description": self.category2.description,
                    "active": self.category2.active,
                },
            ],
        }

        serializer_data = serializer.data
        serializer_data["price"] = float(serializer_data["price"])

        self.assertEqual(serializer_data, expected_data)

    def test_serializer_invalid_data(self):
        data = {
            "description": "Faltando o título",
            "price": "Cem reais",
            "active": True,
            "categories_id": [self.category1.id],
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("price", serializer.errors)
