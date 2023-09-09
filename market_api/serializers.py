from abc import ABC

from rest_framework import serializers
from market_api.models import Product, CartList, Cart


def greater_then_zero_validator(value):
    if value <= 0:
        raise serializers.ValidationError("Price must be greater than zero")


class CartIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(validators=[greater_then_zero_validator])

    class Meta:
        model = Product
        fields = "__all__"


class AddProductToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartList
        fields = ['cart_id', 'product_id']


class UpdateProductInCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartList
        fields = ['cart_id', 'product_id', 'count']
