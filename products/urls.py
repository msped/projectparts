from django.conf.urls import url
from .views import products_view, product_detail, search, get_models, get_gens

urlpatterns = [
    url(r'^$', products_view, name="products"),
    url(r'^(?P<product_id>\d+)/$', product_detail, name="product_detail"),
    url(r'^search/', search, name="search"),
    url(r'^models/', get_models, name="get_models"),
    url(r'^gens/', get_gens, name="get_gens"),
]
