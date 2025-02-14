from rest_framework.exceptions import ValidationError
from django.test import TestCase
from product.serializers import CategorySerializer
from product.factories import CategoryFactory
from product.models import Category


class TestCategorySerializer(TestCase):

    def setUp(self):
        self.category = CategoryFactory(
            title="Eletrônicos",
            slug="eletronicos",
            description="Produtos eletrônicos",
            active=True,
        )

    def test_serializer_valid_data(self):
        serializer = CategorySerializer(instance=self.category)
        expected_data = {
            "title": self.category.title,
            "slug": self.category.slug,
            "description": self.category.description,
            "active": self.category.active,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_serializer_valid_input(self):
        data = {
            "title": "Moda",
            "description": "Produtos de vestuário",
            "active": False,
        }
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertEqual(category.title, data["title"])
        self.assertEqual(category.description, data["description"])
        self.assertEqual(category.active, data["active"])
        self.assertIsNotNone(category.slug)

    def test_serializer_invalid_data(self):
        data = {"description": "Faltando o título", "active": True}
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
