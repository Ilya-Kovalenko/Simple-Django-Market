from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from market_api.serializers import ProductSerializer, AddProductToCartSerializer, UpdateProductInCartSerializer, CartIdSerializer
from market_api.services import CartService, ProductService

import logging

logger = logging.getLogger("market_api_logger")


class ProductView(APIView):
    @staticmethod
    def get(request) -> Response:

        try:
            queryset = ProductService.get_products(request)
            serializer = ProductSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as E:
            logger.warning(E)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def post(request) -> Response:
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            logger.info(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            ProductService.add_product(**serializer.data)
            logger.info("Product with name {}, manufacturer {}, price {} created".format(serializer.data["name"],
                                                                                         serializer.data["manufacturer"],
                                                                                         serializer.data["price"]))
            return Response(status=status.HTTP_200_OK)

        except Exception as E:
            logger.warning(E)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CartView(APIView):
    @staticmethod
    def post(request) -> Response:

        serializer = AddProductToCartSerializer(data=request.data)
        if not serializer.is_valid():
            logger.info(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            CartService.add_product_to_cart(**serializer.data)
            logger.info("Product with id {} added in cart with id {}".format(serializer.data["product_id"],
                                                                             serializer.data["cart_id"]))
            return Response(status=status.HTTP_200_OK)

        except Exception as E:
            logger.warning(E)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request) -> Response:

        serializer = UpdateProductInCartSerializer(data=request.data)
        if not serializer.is_valid():
            logger.info(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            CartService.update_product_count_in_cart(**serializer.data)
            logger.info("Count of product with id {} in cart with id {} changed on {}".format(serializer.data["product_id"],
                                                                                              serializer.data["cart_id"],
                                                                                              serializer.data["count"]))
            return Response(status=status.HTTP_200_OK)

        except Exception as E:
            logger.warning(E)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CartCreateView(APIView):
    @staticmethod
    def post(request) -> Response:

        serializer = CartIdSerializer(data=request.data)
        if not serializer.is_valid():
            logger.info(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            CartService.create_cart(id=serializer.data['id'])
            print(type(Response(status=status.HTTP_200_OK)))
            return Response(status=status.HTTP_200_OK)

        except Exception as E:
            logger.warning(E)
            return Response(status=status.HTTP_400_BAD_REQUEST)
