from django.urls import path
from . import views

urlpatterns = [
    path('product-detail/<int:urunid>/', views.productDetail, name='product-detail'),
]
