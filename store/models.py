from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField


class ProductModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    code = models.PositiveIntegerField(unique=True, blank=True)
    available = models.BooleanField(default=True)
    promotion = models.BooleanField(blank=True)
    image = CloudinaryField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    sale = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    category = models.CharField(max_length=255)
    property = models.JSONField(blank=True)

    favorite = models.ManyToManyField(get_user_model(), blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ProductModel, self).save(*args, **kwargs)


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


class CommentModel(models.Model):
    text = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey("ProductModel", on_delete=models.CASCADE)

    def __str__(self):
        return self.text
