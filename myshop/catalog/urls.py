from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<int:category_id>/', views.product_list_by_category, name='product_list_by_category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path('cart/', views.cart_view, name='cart_view'),
    path('add/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart_view, name='remove_from_cart'),

]
