import uuid
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

import random


class Category(models.Model):
    title = models.CharField(unique=True, max_length=200)
    category_id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True, unique=True
    )
    slug = models.SlugField(unique=True, blank=True)
    featured_product = models.OneToOneField(
        "ProductModel",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="featured_product",
    )
    icon = models.CharField(max_length=100, default=None, blank=True, null=True)

    # def __str__(self):
    #     return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Review(models.Model):
    product = models.ForeignKey(
        "ProductModel", on_delete=models.CASCADE, related_name="reviews"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="description")
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class ProductModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True, unique=True
    )
    code = models.PositiveIntegerField(
        unique=True,
        blank=True,
    )
    available = models.BooleanField(default=True)
    promotion = models.BooleanField(blank=True)
    image = CloudinaryField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    sale = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    bonus = models.PositiveIntegerField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="products",
    )
    property = models.JSONField(
        blank=True,
        null=True,
    )

    favorite = models.ManyToManyField(get_user_model(), blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductModel, self).save(*args, **kwargs)


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Cartitems(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items", null=True, blank=True
    )
    product = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="cartitems",
    )
    quantity = models.PositiveSmallIntegerField(default=0)


class Order(models.Model):

    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED = "F"

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    pending_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default="PAYMENT_STATUS_PENDING"
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.pending_status


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.product.name


# class ShippingAddressModel(models.Model):
#     address = models.CharField(max_length=1024, null=True)
#     city = models.CharField(max_length=200, null=True)
#     zipcode = models.CharField(max_length=200, null=True)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.address


# class OrderModel(models.Model):
#     products_ids = models.JSONField()
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     phone = models.CharField(max_length=20)
#     email = models.EmailField(max_length=255)
#     final_sum = models.FloatField(default=0)
#     address = models.ForeignKey(
#         ShippingAddressModel, on_delete=models.SET_NULL, blank=True, null=True
#     )
#     products = models.ManyToManyField(ProductModel)
#     date_created = models.DateTimeField(auto_now_add=True)


# class CommentModel(models.Model):
#     text = models.TextField()
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     product = models.ForeignKey("ProductModel", on_delete=models.CASCADE)

#     def __str__(self):
#         return self.text
