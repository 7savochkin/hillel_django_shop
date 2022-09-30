from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/item')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/category')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    price = models.PositiveIntegerField()
    sku = models.CharField(max_length=64)


class Discount(models.Model):
    amount = models.PositiveIntegerField()
    code = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    discount_type = models.PositiveSmallIntegerField(
        choices=[(0, 'In money'), (1, 'In percent')])

