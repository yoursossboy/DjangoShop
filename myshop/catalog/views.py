from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product
from django.shortcuts import render, redirect
from .models import Product
from .cart import add_to_cart, remove_from_cart, get_cart_items, get_total_price

def product_list(request):
    # Получаем все категории
    categories = Category.objects.all()
    
    # Получаем все товары
    products = Product.objects.all()
    
    return render(request, 'catalog/product_list.html', {
        'categories': categories,
        'products': products,
    })

def product_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)  # Получаем категорию по id
    products = Product.objects.filter(category=category)  # Получаем товары, связанные с этой категорией
    return render(request, 'catalog/product_list.html', {
        'category': category,
        'products': products,
        'categories': Category.objects.all()  # Передаем все категории
    })

def product_detail(request, product_id):
    """Просмотр подробной информации о товаре"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        # Добавление товара в корзину при POST-запросе
        cart = cart(request)
        cart.add(product)
        return redirect('cart_view')
    
    return render(request, 'catalog/product_detail.html', {'product': product})
    

def add_to_cart_view(request, product_id):
    """ Добавить товар в корзину """
    add_to_cart(request, product_id)
    return redirect('cart_view')  # Перенаправление на страницу корзины

def remove_from_cart_view(request, product_id):
    """ Удалить товар из корзины """
    remove_from_cart(request, product_id)
    return redirect('cart_view')  # Перенаправление на страницу корзины

def cart_view(request):
    """ Страница корзины """
    cart = get_cart_items(request)
    total_price = get_total_price(request)
    return render(request, 'catalog/cart.html', {'cart': cart, 'total_price': total_price})
