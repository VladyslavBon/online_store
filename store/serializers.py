from rest_framework import serializers
from django.contrib.auth import get_user_model


from .models import ProductModel, ShippingAddressModel, OrderModel, CommentModel


class ProductModelSerializer(serializers.ModelSerializer):
    image = serializers.URLField(source="image.url", read_only=True)

    class Meta:
        model = ProductModel
        fields = [
            "id",
            "title",
            "slug",
            "code",
            "available",
            "promotion",
            "image",
            "price",
            "sale",
            "bonus",
            "category",
            "property",
        ]


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "image"]


class ProductCommentSerializer(serializers.ModelSerializer):
    user = UserCommentSerializer(read_only=True)

    class Meta:
        model = CommentModel
        fields = ["text", "user"]


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ["text", "product"]

    def create(self, validated_data):
        comment = CommentModel.objects.create(
            text=validated_data["text"],
            product=validated_data["product"],
            user=self.context["request"].user,
        )

        return comment

    def update(self, instance, validated_data):
        instance.text = validated_data["text"]
        instance.save()

        return instance


class FavoriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ["favorite"]
        lookup_field = "slug"


class OneProductSerializer(serializers.ModelSerializer):
    image = serializers.URLField(source="image.url", read_only=True)
    comments = ProductCommentSerializer(
        many=True, read_only=True, source="commentmodel_set"
    )

    class Meta:
        model = ProductModel
        fields = [
            "id",
            "title",
            "slug",
            "code",
            "available",
            "promotion",
            "image",
            "price",
            "sale",
            "bonus",
            "property",
        ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddressModel
        fields = "__all__"


class OrderSerializerAnonym(serializers.ModelSerializer):
    address = AddressSerializer()
    products = ProductModelSerializer(read_only=True, many=True)

    class Meta:
        model = OrderModel
        fields = "__all__"

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        address = ShippingAddressModel.objects.create(**address_data)

        total = 0
        ordered_ids = dict(
            sorted(
                [
                    (int(key), value)
                    for key, value in validated_data["products_ids"].items()
                ]
            )
        )
        query = ProductModel.objects.filter(id__in=ordered_ids.keys()).order_by("id")

        total = sum(
            [
                query.values()[ind]["price"] * list(ordered_ids.values())[ind]
                for ind in range(len(query))
            ]
        )

        order = OrderModel.objects.create(
            **validated_data, final_sum=total, address=address
        )

        for product in query:
            order.products.add(product)

        return order
