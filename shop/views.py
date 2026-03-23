from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal

from .models import Product, CartItem
from .forms import ProductForm

# 1. PRODUCT LIST: DYNAMIC CATEGORIES + PAGINATION
def product_list(request):
    products_list = Product.objects.all().order_by('-id')
    
    # Logic to fetch only categories that have products assigned to them
    categories = Product.objects.values_list('category', flat=True).distinct()
    
    paginator = Paginator(products_list, 6) # Requirement: Handle large datasets
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'categories': categories, # For the Sidebar loop
    }
    return render(request, 'shop/product_list.html', context)

# 2. SEARCH & FILTERING: DYNAMIC CATEGORIES + PAGINATION
def product_search(request):
    query = request.GET.get('search')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products_list = Product.objects.all()
    # Keep sidebar consistent even on search pages
    categories = Product.objects.values_list('category', flat=True).distinct()

    if query:
        products_list = products_list.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if category:
        products_list = products_list.filter(category__iexact=category)

    if min_price:
        products_list = products_list.filter(price__gte=min_price)
    if max_price:
        products_list = products_list.filter(price__lte=max_price)

    paginator = Paginator(products_list, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'category_name': category
    }
    return render(request, 'shop/product_search.html', context)

# 3. PRODUCT DETAIL
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    # Exclude current product from "Related Products" list
    all_products = Product.objects.all().exclude(id=id)[:4]
    return render(request, 'shop/product_detail.html', {'product': product, 'products': all_products})

# 4. ADD PRODUCT: SECURE ACCESS
@login_required 
def add_product(request):
    if request.method == 'POST':
        # FILES required for image handling
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    
    return render(request, 'shop/add_product.html', {'form': form})

# 5. USER AUTHENTICATION: SIGNUP
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})

# 6. CART MANAGEMENT
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user if request.user.is_authenticated else None,
        product=product
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('cart_page')

def view_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        # Fallback for session users
        cart_items = CartItem.objects.all()

    subtotal = sum((item.quantity * item.product.price for item in cart_items), Decimal('0.00'))
    tax = Decimal('14.00')
    discount = Decimal('60.00')
    
    if cart_items.exists():
        total = (subtotal + tax) - discount
    else:
        total = Decimal('0.00')

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'discount': discount,
        'total': total,
        'products': Product.objects.all()[:4],
    }
    return render(request, 'shop/cart.html', context)