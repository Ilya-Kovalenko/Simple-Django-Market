from rest_framework.test import APITestCase
from market_api.models import Cart, CartList, Product


class TestProduct(APITestCase):

    def test_product_post(self):
        response = self.client.post('/product', {"name": "test_name",
                                                 "manufacturer": "test_manufacturer",
                                                 "price": 111})
        self.assertEqual(response.status_code, 200)

    def test_product_get(self):
        params = {"price_min": 1,
                  "price_max": 1000,
                  "sorting": "name_up"}
        response = self.client.get('/product', params=params)
        self.assertEqual(response.status_code, 200)

    def test_product_filter(self):
        Product.objects.create(name='test_name_1', manufacturer='test_manufacturer', price=100.0)
        Product.objects.create(name='test_name_2', manufacturer='test_manufacturer', price=200.0)

        response = self.client.get('/product', {"price_min": 1,
                                                "price_max": 1000,
                                                "sorting": "price_down"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['price'], 200.0)


class TestCart(APITestCase):

    def test_cart_post(self):
        Product.objects.create(name='test_name', manufacturer='test_manufacturer', price=100.0)
        Cart.objects.create()

        response = self.client.post('/cart', {"product_id": 1,
                                              "cart_id": 1})

        self.assertEqual(response.status_code, 200)

    def test_cart_put(self):
        Product.objects.create(name='test_name', manufacturer='test_manufacturer', price=100.0)
        Product.objects.create(name='test_name_2', manufacturer='test_manufacturer', price=110.0)
        Cart.objects.create()

        self.client.post('/cart', {"product_id": 1,
                                   "cart_id": 1})
        self.client.post('/cart', {"product_id": 2,
                                   "cart_id": 1})

        self.client.put('/cart', {"product_id": 1,
                                  "cart_id": 1,
                                  "count": 9})
        response = self.client.put('/cart', {"product_id": 2,
                                             "cart_id": 1,
                                             "count": 1})

        cart_list_1 = CartList.objects.get(id=1)
        cart_list_2 = CartList.objects.get(id=2)
        cart = Cart.objects.get(id=1)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(cart.count, 12)
        self.assertEqual(cart.price, 1220.0)

        self.assertEqual(cart_list_1.count, 10)
        self.assertEqual(cart_list_2.count, 2)

