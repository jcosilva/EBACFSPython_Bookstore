import json

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory, OrderFactory
from product.models import Product

class TestProductViewSet(APITestCase):

    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory(title='books')

        self.product = ProductFactory(
            title='pro controller',
            price=200.00,
            category=[self.category]
        )
    
    def test_get_all_product(self):
        response = self.client.get(
            reverse('product-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_data = json.loads(response.content)

        self.assertEqual(product_data[0]['title'], self.product.title)
        self.assertEqual(product_data[0]['price'], self.product.price)
        self.assertEqual(product_data[0]['active'], self.category.active),
        self.assertEqual(product_data[0]['category'][0]['title'], self.category.title)
    
    def test_create_product(self):
        category = CategoryFactory()
        data = json.dumps({
            'title': 'notebook',
            'price': 800.00,
            'categories_id': [category.id]
        })

        response = self.client.post(
            reverse('product-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_product = Product.objects.get(title='notebook')

        self.assertEqual(created_product.title, 'notebook')
        self.assertEqual(created_product.price, 800.00)
