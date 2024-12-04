# catalog/cart.py
from decimal import Decimal
from django.conf import settings
from catalog.models import Product

def get_cart(request):
    """ Получить корзину из сессии. """
    cart = request.session.get('cart', {})
    return cart

def add_to_cart(request, product_id, quantity=1):
    """ Добавить товар в корзину. """
    cart = get_cart(request)
    product = Product.objects.get(id=product_id)
    
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': quantity,
            'image': product.image.url if product.image else None,
        }

    request.session['cart'] = cart  # Сохраняем корзину в сессии

def remove_from_cart(request, product_id):
    """ Удалить товар из корзины. """
    cart = get_cart(request)
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart  # Сохраняем изменения в сессии

def get_total_price(request):
    """ Получить общую цену товаров в корзине. """
    total = Decimal(0)
    cart = get_cart(request)
    for item in cart.values():
        total += Decimal(item['price']) * item['quantity']
    return total

def get_cart_items(request):
    """ Получить все товары в корзине. """
    cart = get_cart(request)
    return cart
