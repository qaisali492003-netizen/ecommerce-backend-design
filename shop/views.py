from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal

from .models import Product, CartItem
from .forms import ProductForm

# 1. PRODUCT LIST
def product_list(request):
    products_list = Product.objects.all().order_by('-id')
    categories = Product.objects.values_list('category', flat=True).distinct()
    paginator = Paginator(products_list, 6) 
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'shop/product_list.html', {'products': products, 'categories': categories})

# 2. SEARCH
def product_search(request):
    query = request.GET.get('search')
    products_list = Product.objects.all()
    if query:
        products_list = products_list.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'shop/product_search.html', {'products': products_list})

# 3. PRODUCT DETAIL
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product, 'products': Product.objects.all()[:4]})

# 4. ADD TO CART
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('cart_page')

# 5. VIEW CART (Variable sync with HTML)
def view_cart(request):
    user = request.user if request.user.is_authenticated else None
    cart_items = CartItem.objects.filter(user=user)
    
    subtotal = Decimal('0.00')
    for item in cart_items:
        # Convert to string first to avoid float-precision errors
        price = Decimal(str(item.product.price))
        subtotal += item.quantity * price

    tax = Decimal('14.00') if cart_items.exists() else Decimal('0.00')
    discount = Decimal('60.00') if cart_items.exists() else Decimal('0.00')
    
    # Final total calculation
    total = (subtotal + tax) - discount
    if total < 0: total = Decimal('0.00')

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'discount': discount,
        'total': total, # Matches {{ total }} in HTML
        'products': Product.objects.all()[:4],
    })

# 6. REMOVE & CLEAR
def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('cart_page')

def clear_cart(request):
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user).delete()
    return redirect('cart_page')

# AUTH & ADD PRODUCT
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(); login(request, user)
            return redirect('product_list')
    else: form = UserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})

@login_required 
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid(): form.save(); return redirect('product_list')
    else: form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})