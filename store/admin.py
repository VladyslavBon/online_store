from django.contrib import admin

from .models import ProductModel, ShippingAddressModel, OrderModel, CommentModel


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "price", "manufacturer", "guarantee", "info"]


@admin.register(ShippingAddressModel)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ["address", "city", "zipcode", "date_added"]


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "date_created"]


@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "user", "product"]
