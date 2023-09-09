from market_api.models import Product, Cart, CartList
from django.shortcuts import get_object_or_404


class CartService:
    @staticmethod
    def create_cart(id: int) -> None:
        Cart.objects.create(id=id)

    @staticmethod
    def update_cart(product_id: int, cart_id: int, count: int) -> None:
        cart = Cart.objects.get(id=cart_id)
        product = get_object_or_404(Product, id=product_id)

        cart.price += product.price * count
        cart.count += count
        cart.save()

    @staticmethod
    def add_product_to_cart(product_id: int, cart_id: int) -> None:
        cart = Cart.objects.get(id=cart_id)
        product = get_object_or_404(Product, id=product_id)

        CartList.objects.create(cart_id=cart, product_id=product)
        CartService.update_cart(product_id=product_id, cart_id=cart_id, count=1)

    @staticmethod
    def update_product_count_in_cart(product_id: int, cart_id: int, count: int) -> None:
        if count == 0:
            return

        cart_list = CartList.objects.get(cart_id=cart_id, product_id=product_id)

        new_count = cart_list.count + count

        if new_count > 0:
            cart_list.count += count
            cart_list.save()
            CartService.update_cart(product_id=product_id, cart_id=cart_id, count=count)

        elif new_count == 0:
            cart_list.delete()
            CartService.update_cart(product_id=product_id, cart_id=cart_id, count=count)

        else:
            raise ValueError("Cart with id {} does not have count of product with id {}".format(cart_id, product_id))
