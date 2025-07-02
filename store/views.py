from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Category, Product

def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:8]
    categories = Category.objects.all()
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)

def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    
    # Sorting
    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'popular':
        products = products.order_by('-popularity')
    
    # Filter by discount
    if request.GET.get('discount'):
        products = products.filter(discount__gt=0)
    
    context = {
        'category': category,
        'products': products,
        'current_sort': sort,
    }
    return render(request, 'store/category.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__name__icontains=query)
    ).distinct()
    
    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'store/search.html', context)

def cart(request):
    cart_items = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart_items)
    
    total = sum(product.discounted_price for product in products)
    
    context = {
        'cart_items': products,
        'total': total,
    }
    return render(request, 'store/cart.html', context)

def wishlist(request):
    wishlist_items = request.session.get('wishlist', [])
    products = Product.objects.filter(id__in=wishlist_items)
    
    context = {
        'wishlist_items': products,
    }
    return render(request, 'store/wishlist.html', context)

# API Views for Cart and Wishlist
def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart_items = request.session.get('cart', [])
        if product_id not in cart_items:
            cart_items.append(product_id)
            request.session['cart'] = cart_items
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        wishlist_items = request.session.get('wishlist', [])
        if product_id not in wishlist_items:
            wishlist_items.append(product_id)
            request.session['wishlist'] = wishlist_items
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def move_to_cart(request, product_id):
    if request.method == 'POST':
        wishlist_items = request.session.get('wishlist', [])
        cart_items = request.session.get('cart', [])
        
        if product_id in wishlist_items:
            wishlist_items.remove(product_id)
            if product_id not in cart_items:
                cart_items.append(product_id)
            
            request.session['wishlist'] = wishlist_items
            request.session['cart'] = cart_items
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def move_to_wishlist(request, product_id):
    if request.method == 'POST':
        cart_items = request.session.get('cart', [])
        wishlist_items = request.session.get('wishlist', [])
        
        if product_id in cart_items:
            cart_items.remove(product_id)
            if product_id not in wishlist_items:
                wishlist_items.append(product_id)
            
            request.session['cart'] = cart_items
            request.session['wishlist'] = wishlist_items
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart_items = request.session.get('cart', [])
        if product_id in cart_items:
            cart_items.remove(product_id)
            request.session['cart'] = cart_items
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def remove_from_wishlist(request, product_id):
    if request.method == 'POST':
        wishlist_items = request.session.get('wishlist', [])
        if product_id in wishlist_items:
            wishlist_items.remove(product_id)
            request.session['wishlist'] = wishlist_items
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
