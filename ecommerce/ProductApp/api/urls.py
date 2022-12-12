from django.urls import path
from ProductApp.api import views as api_views


urlpatterns = [
    path('p/<int:id>/', api_views.ProductsListAPIView.as_view(), name="product"),
    path('products/', api_views.ProductsSearchListAPIView.as_view(), name="products"),
    path('pfilter/', api_views.ProductsFilterListAPIView.as_view(), name="pfilter"),
]