from rest_framework import serializers
from product.models import Product
from order.models import Order
from product.serializers.product_serializer import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, many=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, many=True
    )
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([product.price for product in instance.product.all()])
        return total

    class Meta:
        model = Order
        fields = ["product", "total", "user", "product_id"]
        extra_kwargs = {"product": {"required": False}}

    def validate_product_id(self, value):
        if not value:
            raise serializers.ValidationError(
                "O pedido deve conter pelo menos um produto."
            )
        return value

    def create(self, validated_data):
        product_data = validated_data.pop("product_id")
        user_data = validated_data.pop("user")

        order = Order.objects.create(user=user_data)
        for product in product_data:
            order.product.add(product)

        return order
