from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal

from .models import Product, CartItem
from .forms import ProductForm # Make sure you have a forms.py with ProductForm!

# 1. PRODUCT LIST
def product_list(request):
    products_qs = Product.objects.all().order_by('-id')
    categories = Product.objects.values_list('category', flat=True).distinct()
    
    paginator = Paginator(products_qs, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    return render(request, 'shop/product_list.html', {
        'products': products, 
        'categories': categories
    })

# 2. PRODUCT SEARCH
def product_search(request):
    query = request.GET.get('search')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()
    return render(request, 'shop/product_search.html', {'products': products})

# 3. HELPER FOR ZERO-INTERFERENCE CART
def get_cart_items(request):
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user)
    if not request.session.session_key:
        request.session.create()
    return CartItem.objects.filter(session_key=request.session.session_key)

# 4. ADD TO CART
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    else:
        if not request.session.session_key:
            request.session.create()
        item, created = CartItem.objects.get_or_create(session_key=request.session.session_key, product=product)
    
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart_page')

# 5. VIEW CART
def view_cart(request):
    cart_items = get_cart_items(request)
    subtotal = sum(item.total_price() for item in cart_items)
    
    tax = Decimal('14.00') if subtotal > 0 else Decimal('0.00')
    discount = Decimal('60.00') if subtotal > 100 else Decimal('0.00')
    total = max(Decimal('0.00'), (subtotal + tax) - discount)

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'discount': discount,
        'total': total,
        'products': Product.objects.all()[:4]
    })

# 6. REMOVE & CLEAR
def remove_from_cart(request, product_id):
    get_cart_items(request).filter(product_id=product_id).delete()
    return redirect('cart_page')

def clear_cart(request):
    get_cart_items(request).delete()
    return redirect('cart_page')

# 7. PRODUCT DETAIL
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})

# 8. ADD PRODUCT (Admin/Management)
@login_required 
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})

# 9. GATED PAGES
@login_required
def checkout(request):
    return render(request, 'shop/checkout.html')

@login_required
def profile_view(request):
    return render(request, 'shop/profile.html', {'user': request.user})

# 10. AUTH
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