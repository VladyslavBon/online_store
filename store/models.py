from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model


class ProductModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    price = models.FloatField()
    manufacturer = models.CharField(max_length=255)
    guarantee = models.IntegerField()
    info = models.JSONField(blank=True)

    favorite = models.ManyToManyField(get_user_model(), blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductModel, self).save(*args, **kwargs)


class CommentModel(models.Model):
    text = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey("ProductModel", on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class ShippingAddressModel(models.Model):
    address = models.CharField(max_length=1024, null=True)
    city = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class OrderModel(models.Model):
    products_ids = models.JSONField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    final_sum = models.FloatField(default=0)
    address = models.ForeignKey(
        ShippingAddressModel, on_delete=models.SET_NULL, blank=True, null=True
    )
    products = models.ManyToManyField(ProductModel)
    date_created = models.DateTimeField(auto_now_add=True)
