from django.test import TestCase
from order.models import Order
from product.models import Product
from order.serializers import OrderSerializer
from order.factories import OrderFactory, UserFactory
from product.factories import ProductFactory
from rest_framework.exceptions import ValidationError


class TestOrderSerializer(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.product1 = ProductFactory(title="Mouse Gamer", price=200.00)
        self.product2 = ProductFactory(title="Teclado Mecânico", price=350.00)

        self.order = OrderFactory(user=self.user)
        self.order.product.add(self.product1, self.product2)

    def test_order_serializer_valid_data(self):
        serializer = OrderSerializer(instance=self.order)

        expected_data = {
            "product": [
                {
                    "id": self.product1.id,
                    "title": self.product1.title,
                    "description": self.product1.description,
                    "price": float(self.product1.price),
                    "active": self.product1.active,
                    "category": [],
                },
                {
                    "id": self.product2.id,
                    "title": self.product2.title,
                    "description": self.product2.description,
                    "price": float(self.product2.price),
                    "active": self.product2.active,
                    "category": [],
                },
            ],
            "total": float(self.product1.price + self.product2.price),
            "user": self.user.id,
        }

        serializer_data = serializer.data
        serializer_data["total"] = float(
            serializer_data["total"]
        )  # Garantir que total seja float

        self.assertEqual(serializer_data, expected_data)

    def test_order_serializer_valid_input(self):
        data = {
            "product_id": [self.product1.id, self.product2.id],
            "user": self.user.id,
        }

        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        order = serializer.save()

        self.assertEqual(order.user, self.user)
        self.assertEqual(set(order.product.all()), {self.product1, self.product2})

    def test_order_serializer_invalid_data(self):
        data = {
            "product_id": [],
            "user": self.user.id,
        }

        serializer = OrderSerializer(data=data)
        is_valid = serializer.is_valid()

        self.assertFalse(is_valid)
        self.assertIn("product_id", serializer.errors)
