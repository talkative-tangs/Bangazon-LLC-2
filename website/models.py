from django.contrib.auth.models import User
from django.db import models
from datetime import datetime, date


# Create your models here.
class Customer(models.Model):
      '''A user that can place an order/a buyer'''
      user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
      )
      address = models.CharField(max_length=100, blank=False)
      phoneNum = models.IntegerField(blank=False)
      deletedDate = models.DateField(default=None, blank=True, null=True)

      def __str__(self):
        '''string method that returns Customer's full name'''

        full_name = (f"{self.user.first_name} {self.user.last_name}")
        return full_name


class ProductType(models.Model):
      '''Various Product Categories'''
      name =  models.TextField(blank=False)
      deletedDate = models.DateField(default=None, blank=True, null=True)

      def __str__(self):
            '''string method that returns the product type name'''

            return self.name

class Product(models.Model):
      '''An item that a User can Sell or Buy'''

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
        on_delete=models.CASCADE, null=True
      )
      deletedDate = models.DateField(default=None, blank=True, null=True)

      def __str__(self):
        '''string method that returns Product title'''

        return self.seller.user.first_name + "'s " + self.title

class PaymentType(models.Model):
      '''A payment type saved by the buyer for use with orders'''

      name = models.CharField(max_length=50, blank=False)
      accountNum = models.IntegerField(blank=False)
      buyer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
      )
      deletedDate = models.DateField(default=None, blank=True, null=True)

      def __str__(self):
            '''string method that returns the payment type name'''

            return self.buyer.user.first_name + "'s " + self.name

class Order(models.Model):
      '''An order placed by the buying/logged in user'''

      buyer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
      )
      paymentType = models.ForeignKey(
        PaymentType,
        on_delete=models.PROTECT
      )
      product = models.ManyToManyField(Product, through='ProductOrder')
      deletedDate = models.DateField(default=None, blank=True, null=True)

      def __str__(self):
        '''string method that returns the Order id'''

        return str(self.id)

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

      def __str__(self):
        '''string method that returns the ProductOrder id'''

        return str(self.id)