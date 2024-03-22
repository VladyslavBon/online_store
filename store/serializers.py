from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction


from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "title", "slug"]


class ProductSerializerPOST(serializers.ModelSerializer):
    # image = serializers.URLField(source="image.url", read_only=True)
    # category = CategorySerializer(read_only=True)

    class Meta:
        model = ProductModel
        fields = [
            "id",
            "name",
            "description",
            "slug",
            "available",
            "price",
            "image",
            "promotion",
            "sale",
            "bonus",
            "property",
            "category",
        ]

    def create(self, validated_data):
        category_data = validated_data.pop("category")
        category = Category.objects.get(category_id=category_data.category_id)
        product = ProductModel.objects.create(category=category, **validated_data)
        return product

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.URLField(source="image.url", read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = ProductModel
        fields = [
            "id",
            "name",
            "description",
            "slug",
            "available",
            "price",
            "image",
            "promotion",
            "sale",
            "bonus",
            "property",
            "category",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "date_created", "name", "description"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ["id", "name", "price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = Cartitems
        fields = ["id", "cart", "product", "quantity", "sub_total"]

    def total(self, cartitem: Cartitems):
        return cartitem.quantity * cartitem.product.price


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()

    def validate_product_id(self, value):
        if not ProductModel.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                "There is no product associated with the given ID"
            )

        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cartitem = Cartitems.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()

            self.instance = cartitem

        except:

            self.instance = Cartitems.objects.create(
                cart_id=cart_id, **self.validated_data
            )

        return self.instance

    class Meta:
        model = Cartitems
        fields = ["id", "product_id", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Cartitems
        fields = ["quantity"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name="main_total")

    class Meta:
        model = Cart
        fields = ["id", "items", "grand_total"]

    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "placed_at", "pending_status", "owner", "items"]


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("This cart_id is invalid")

        elif not Cartitems.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError("Sorry your cart is empty")

        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id = self.context["user_id"]
            order = Order.objects.create(owner_id=user_id)
            cartitems = Cartitems.objects.filter(cart_id=cart_id)
            orderitems = [
                OrderItem(order=order, product=item.product, quantity=item.quantity)
                for item in cartitems
            ]
            OrderItem.objects.bulk_create(orderitems)
            # Cart.objects.filter(id=cart_id).delete()
            return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["pending_status"]


# class ProductModelSerializer(serializers.ModelSerializer):
#     image = serializers.URLField(source="image.url", read_only=True)

#     class Meta:
#         model = ProductModel
#         fields = [
#             "id",
#             "title",
#             "slug",
#             "available",
#             "promotion",
#             "image",
#             "price",
#             "sale",
#             "bonus",
#             "category",
#             "property",
#         ]


# class UserCommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ["email", "image"]


# class ProductCommentSerializer(serializers.ModelSerializer):
#     user = UserCommentSerializer(read_only=True)

#     class Meta:
#         model = CommentModel
#         fields = ["text", "user"]


# class CommentCreateUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CommentModel
#         fields = ["text", "product"]

#     def create(self, validated_data):
#         comment = CommentModel.objects.create(
#             text=validated_data["text"],
#             product=validated_data["product"],
#             user=self.context["request"].user,
#         )

#         return comment

#     def update(self, instance, validated_data):
#         instance.text = validated_data["text"]
#         instance.save()

#         return instance


# class FavoriteProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductModel
#         fields = ["favorite"]
#         lookup_field = "slug"


# class OneProductSerializer(serializers.ModelSerializer):
#     image = serializers.URLField(source="image.url", read_only=True)
#     comments = ProductCommentSerializer(
#         many=True, read_only=True, source="commentmodel_set"
#     )

#     class Meta:
#         model = ProductModel
#         fields = [
#             "id",
#             "title",
#             "slug",
#             "code",
#             "available",
#             "promotion",
#             "image",
#             "price",
#             "sale",
#             "bonus",
#             "property",
#         ]


# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ShippingAddressModel
#         fields = "__all__"


# class OrderSerializerAnonym(serializers.ModelSerializer):
#     address = AddressSerializer()
#     products = ProductModelSerializer(read_only=True, many=True)

#     class Meta:
#         model = OrderModel
#         fields = "__all__"

#     def create(self, validated_data):
#         address_data = validated_data.pop("address")
#         address = ShippingAddressModel.objects.create(**address_data)

#         total = 0
#         ordered_ids = dict(
#             sorted(
#                 [
#                     (int(key), value)
#                     for key, value in validated_data["products_ids"].items()
#                 ]
#             )
#         )
#         query = ProductModel.objects.filter(id__in=ordered_ids.keys()).order_by("id")

#         total = sum(
#             [
#                 query.values()[ind]["price"] * list(ordered_ids.values())[ind]
#                 for ind in range(len(query))
#             ]
#         )

#         order = OrderModel.objects.create(
#             **validated_data, final_sum=total, address=address
#         )

#         for product in query:
#             order.products.add(product)

#         return order
