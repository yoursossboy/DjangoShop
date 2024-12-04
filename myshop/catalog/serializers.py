from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):

    category_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category_name']

    def get_category_name(self, obj):
        return obj.category.name
    
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Вложенный сериализатор для продуктов

    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)  # Вложенный сериализатор для элементов заказа

    class Meta:
        model = Order
        fields = ['name', 'email', 'total_price', 'order_items', 'order_date']