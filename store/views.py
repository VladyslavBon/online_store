from django.http import HttpResponse
from django.views.generic import TemplateView
from django.db.models import Q, F


from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.parsers import MultiPartParser, JSONParser
import cloudinary.uploader


from .models import ProductModel, OrderModel, CommentModel
from .serializers import (
    ProductModelSerializer,
    OrderSerializerAnonym,
    AddressSerializer,
    ShippingAddressModel,
    OneProductSerializer,
    CommentCreateUpdateSerializer,
    FavoriteProductSerializer,
)

from .filters import AllWillBeOneFilter


@api_view(["GET"])
def ApiOverview(request):
    api_urls = {
        "Create product": {
            "endpoint": "/products/create/",
            "methods": "POST",
            "info": "Create product to data base",
            "fields": {
                "title": "",
                "code": "",
                "available": "",
                "promotion": "",
                "image": "image.jpg",
                "price": "",
                "sale": "",
                "bonus": "",
                "property": {
                    "key": "value",
                    "key": "value",
                },
            },
        },
        "Update/Delete product": {
            "endpoint": "/products/detail/<slug>",
            "methods": "GET/PUT/PATCH/DELETE",
            "info": "Update/Delete product in Data Base",
        },
        "List products": {
            "endpoint": "/products/",
            "methods": "GET",
            "info": "Return all products from data base",
        },
        "Search product by slug": {
            "endpoint": "/products/<slug>",
            "methods": "GET",
            "info": "Returns product with given slug",
            "example": "products/amd-ryzen-5600",
        },
        "Search product by symbols in it's name": {
            "endpoint": "/products/search/?title=<title>",
            "methods": "GET",
            "info": "Returns products with given name",
            "example": "/products/search/?title=amd",
        },
        "Filter products by specific conditions": {
            "endpoint": "/products/filter/<conditions>",
            "methods": "GET",
            "info": "Returns products with given conditions",
            "example": "/products/filter/?price=&available=&min_price=&max_price=3499",
        },
        "Registration user": {
            "endpoint": "/accounts/register/",
            "methods": "POST",
            "info": "Registers new user",
            "fields": {
                "email": "",
                "first_name": "",
                "last_name": "",
                "phone_number": "",
                "password": "",
                "password2": "",
            },
        },
        "Login user": {
            "endpoint": "/accounts/login/",
            "methods": "POST",
            "info": "User logins and obtains two tokens, access token need to access API endpoints with permission_classes, refresh needed to create new access token",
            "fields": {"email": "", "password": ""},
            "response": {"refresh": "<some value>", "access": "<some value>"},
        },
        "Access token refresh": {
            "endpoint": "/accounts/login/refresh/",
            "methods": "POST",
            "info": "Requires refresh token to generate new access token and refresh tokens",
            "fields": {"refresh": ""},
            "response": {"refresh": "<some value>", "access": "<some value>"},
        },
        "User profile": {
            "endpoint": "/accounts/profile/",
            "methods": "GET",
            "info": "Shows profile of current logged in user",
            "requires": "access token",
        },
    }
    return Response(api_urls)


class CreateProductView(generics.CreateAPIView):
    """Create product to Data Base"""

    queryset = ProductModel.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductModelSerializer
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        file = request.data.get("image")
        upload_data = cloudinary.uploader.upload(file, folder="online_store")

        if serializer.is_valid():
            serializer.save(image=upload_data["url"])
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
            return Response(serializer.data, status=201)

    def create_multiple(self, request):
        data = request.data

        for product_data in data:
            serializer = self.serializer_class(data=product_data)
            serializer.is_valid(raise_exception=True)

            file = product_data.get("image")
            upload_data = cloudinary.uploader.upload(file, folder="online_store")

            serializer.save(image=upload_data["url"])
        return Response(status=status.HTTP_201_CREATED)


class DetailProductView(generics.RetrieveUpdateDestroyAPIView):
    """Update/Delete product in Data Base"""

    queryset = ProductModel.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductModelSerializer
    lookup_field = "slug"


class GetAllProductsView(generics.ListAPIView):
    """Get list all products in Data Base"""

    queryset = ProductModel.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductModelSerializer

    def get_image(request, product_id):
        product = ProductModel.objects.get(pk=product_id)
        image_url = product.image.url
        response = HttpResponse(image_url)
        return response


class GetProductView(generics.RetrieveAPIView):
    """Get product by slug"""

    queryset = ProductModel.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = OneProductSerializer
    lookup_field = "slug"

    def get_image(request, product_id):
        product = ProductModel.objects.get(pk=product_id)
        image_url = product.image.url
        response = HttpResponse(image_url)
        return response


class SearchProductsView(generics.ListAPIView):
    """Search product by symbols in it's name"""

    permission_classes = (AllowAny,)
    serializer_class = ProductModelSerializer

    def get_queryset(self):
        queryset = ProductModel.objects.all()
        title = self.request.query_params.get("title")
        if title is not None:
            queryset = queryset.filter(Q(title__icontains=title))
        return queryset


class FilterProductsView(generics.ListAPIView):
    """Filter products by specific conditions"""

    queryset = ProductModel.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AllWillBeOneFilter


class AuthOrderApiView(APIView):
    pass


class OrderApiView(APIView):
    """Creates order"""


def post(self, request, *args, **kwargs):
    if request.user.is_authenticated:
        """TO DO for logged in User"""

        return Response("I am Authenticated")

    else:
        serializer = OrderSerializerAnonym(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetOrderApi(generics.RetrieveAPIView):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializerAnonym
    permission_classes = (AllowAny,)
    lookup_field = "id"


class UpdateComment(generics.RetrieveUpdateAPIView):
    queryset = CommentModel.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentCreateUpdateSerializer
    lookup_field = "id"


class CreateComment(generics.CreateAPIView):
    queryset = CommentModel.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentCreateUpdateSerializer


class FavoriteProductUpd(generics.RetrieveUpdateDestroyAPIView):
    """TO DO - create separate Create and Delete"""

    queryset = ProductModel.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug"
