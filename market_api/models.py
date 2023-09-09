from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Cart(BaseModel):
    count = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)


class Product(BaseModel):
    name = models.CharField(max_length=30)
    manufacturer = models.CharField(max_length=30)
    price = models.FloatField()


class CartList(BaseModel):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
