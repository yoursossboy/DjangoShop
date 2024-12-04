import requests

from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from .cart import add_to_cart, remove_from_cart, get_cart_items, get_total_price
from .models import Category, Product, Order, OrderItem
from .forms import OrderForm
from .models import Product
from .serializers import ProductModelSerializer
from django.views.decorators.csrf import csrf_exempt

class DjangoShopAPIView(APIView):
    def get(self, request):
        data = Product.objects.all()
        serializer = ProductModelSerializer(data, many=True)
        return Response(serializer.data)

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

def send_order_to_1c(order):
    url = "http://localhost:8080/заказ"  # URL веб-сервиса 1С
    data = {
        "НомерЗаказа": order.id,
        "Имя": order.name,
        "Почта": order.email,
        "СоставЗаказа": order.get_items()  # Получаем состав заказа
    }
    response = requests.post(url, data=data)

    if response.status_code == 200:
        return True
    else:
        return False

@csrf_exempt
def create_order(request):
    # Получаем товары из корзины
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            # Создаем заказ
            order = Order.objects.create(
                name=name,
                email=email,
                total_price=0
            )

            total_price = 0
            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
                total_price += product.price * quantity

            order.total_price = total_price
            order.save()

            # Отправляем заказ в 1С
            send_order_to_1c(order)

            # Очищаем корзину
            request.session['cart'] = {}

            return render(request, 'order_confirmation.html', {'order': order})

    else:
        form = OrderForm()

    return render(request, 'create_order.html', {'form': form})