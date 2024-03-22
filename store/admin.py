from django.contrib import admin

from .models import *


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductModel, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Cartitems)
admin.site.register(Order)
admin.site.register(OrderItem)
# @admin.register(ProductModel)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = [
#         "id",
#         "title",
#         "slug",
#         "available",
#         "promotion",
#         "image",
#         "price",
#         "sale",
#         "bonus",
#         "property",
#     ]


# @admin.register(ShippingAddressModel)
# class ShippingAddressAdmin(admin.ModelAdmin):
#     list_display = ["address", "city", "zipcode", "date_added"]


# @admin.register(OrderModel)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ["id", "first_name", "last_name", "date_created"]


# @admin.register(CommentModel)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ["id", "text", "user", "product"]
