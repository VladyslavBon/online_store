from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("", views.ApiOverview, name="home"),
    path("products/", views.GetAllProductsView.as_view(), name="get_products"),
    path("products/create/", views.CreateProductView.as_view(), name="create_product"),
    path(
        "products/detail/<slug:slug>",
        views.DetailProductView.as_view(),
        name="update/delete_product",
    ),
    path("products/<slug:slug>", views.GetProductView.as_view(), name="get_product"),
    path(
        "products/search/", views.SearchProductsView.as_view(), name="search_products"
    ),
    path(
        "products/filter/", views.FilterProductsView.as_view(), name="filter_products"
    ),
    path("products/checkout/", views.OrderApiView.as_view()),
    path("products/order/<int:id>", views.GetOrderApi.as_view()),
    path("products/comment/", views.CreateComment.as_view()),
    path("products/comment/<int:id>/", views.UpdateComment.as_view()),
    path("products/favorite/upd/<slug:slug>/", views.FavoriteProductUpd.as_view()),
]
