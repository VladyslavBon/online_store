from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views

app_name = "store"


router = routers.DefaultRouter()

router.register("products", views.ProductsViewSet)
router.register("categories", views.CategoryViewSet)
router.register("carts", views.CartViewSet)
router.register("orders", views.OrderViewSet, basename="orders")


product_router = routers.NestedDefaultRouter(router, "products", lookup="slug")
product_router.register("reviews", views.ReviewViewSet, basename="product-reviews")


cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", views.CartItemViewSet, basename="cart-items")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls)),
    path("", include(cart_router.urls)),
]
# urlpatterns = [
#     path("", views.ApiOverview, name="home"),
#     path("products/", views.GetAllProductsView.as_view(), name="get_products"),
#     path("products/create/", views.CreateProductView.as_view(), name="create_product"),
#     path(
#         "products/detail/<slug:slug>",
#         views.DetailProductView.as_view(),
#         name="update/delete_product",
#     ),
#     path("products/<slug:slug>", views.GetProductView.as_view(), name="get_product"),
#     path(
#         "products/search/",
#         views.SearchProductsView.as_view(),
#         name="search_products",
#     ),
#     path(
#         "products/filter/", views.FilterProductsView.as_view(), name="filter_products"
#     ),
#     path("products/checkout/", views.CreateOrderView.as_view(), name="create_order"),
#     path("products/order/<int:id>", views.GetOrderView.as_view(), name="get_order"),
#     path("products/comment/", views.CreateComment.as_view()),
#     path("products/comment/<int:id>/", views.UpdateComment.as_view()),
#     path("products/favorite/upd/<slug:slug>/", views.FavoriteProductUpd.as_view()),
# ]
