from django.conf.urls import url
from .views import products_view, product_detail

urlpatterns = [
    url(r'^$', products_view, name="products"),
    url(r'^detail/(?P<product_id>\d+)/$', product_detail, name="product_detail")
]
