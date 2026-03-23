from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. Product Listing & Home
    path('', views.product_list, name='product_list'),
    path('search/', views.product_search, name='product_search'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    
    # 2. Cart Management
    path('cart/', views.view_cart, name='cart_page'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    
    # 3. Gated Pages (Require Login)
    path('checkout/', views.checkout, name='checkout'),  # <-- New
    path('profile/', views.profile_view, name='profile'), # <-- New
    
    # 4. Product Management
    path('add-product/', views.add_product, name='add_product'),
    
    # 5. Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='product_list'), name='logout'),
]