from django.contrib.auth.models import User
from django.db import models

from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE



# Create your models here.
class Customer(models.Model):
      '''A user that can place an order/a buyer'''
      user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
      )
      address = models.CharField(max_length=100, blank=False)
      phoneNum = models.IntegerField(blank=False)


class ProductType(models.Model):
      '''Various Product Categories'''
      name =  models.TextField(blank=False)


class Product(SafeDeleteModel):
      '''An item that a User can Sell or Buy'''
      _safedelete_policy = SOFT_DELETE_CASCADE

      seller = models.ForeignKey(
          Customer,
          on_delete=models.CASCADE,
      )
      title = models.CharField(max_length=100, blank=False)
      description = models.TextField(blank=False, null=True)
      price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)
      quantity = models.IntegerField(blank=False)
      productType = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
      )

class PaymentType(SafeDeleteModel):
      '''A payment type saved by the buyer for use with orders'''
      _safedelete_policy = SOFT_DELETE_CASCADE

      name = models.CharField(max_length=50, blank=False)
      accountNum = models.IntegerField(blank=False)
      buyer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
      )

class Order(SafeDeleteModel):
      '''An order placed by the buying/logged in user'''
      _safedelete_policy = SOFT_DELETE_CASCADE

      buyer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
      )
      paymentType = models.ForeignKey(
        PaymentType,
        on_delete=models.PROTECT
      )
      product = models.ManyToManyField(Product, through='ProductOrder')

class ProductOrder(models.Model):
      '''A join table linking the product being sold to the order being placed'''
      product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
      )
      order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
      )