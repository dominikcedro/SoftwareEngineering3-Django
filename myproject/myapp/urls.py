from . import views
from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView

urlpatterns = [
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('user/products/', ProductListView.as_view(), name='product_list'),
    path('user/products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('user/products/new/', ProductCreateView.as_view(), name='product_create'),
]