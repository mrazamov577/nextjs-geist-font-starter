from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:category_slug>/', views.category_products, name='category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('search/', views.search, name='search'),
    
    # API endpoints for cart and wishlist
    path('api/add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('api/add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('api/move-to-cart/<int:product_id>/', views.move_to_cart, name='move_to_cart'),
    path('api/move-to-wishlist/<int:product_id>/', views.move_to_wishlist, name='move_to_wishlist'),
    path('api/remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('api/remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
