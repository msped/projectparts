from django.urls import path
from .views import products_view, productDetail, get_models, get_gens

urlpatterns = [
    path('', products_view, name="products"),
    path('<slug:slug>', productDetail.as_view(), name="product_detail"),
    path('models/', get_models, name="get_models"),
    path('gens/', get_gens, name="get_gens"),
]
