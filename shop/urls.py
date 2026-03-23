from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. Product Listing & Home
    path('', views.product_list, name='product_list'),
    
    # 2. Search & Filtering
    path('search/', views.product_search, name='product_search'),
    
    # 3. Product Detail
    path('<int:id>/', views.product_detail, name='product_detail'),
    
    # 4. Cart Management
    path('cart/', views.view_cart, name='cart_page'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    # 5. Product Management (Week 3 Requirement)
    path('add-product/', views.add_product, name='add_product'),
    
    # 6. Authentication (Week 3 Requirement)
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='product_list'), name='logout'),
]