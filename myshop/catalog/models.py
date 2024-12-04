from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Ожидает оплаты')

    def __str__(self):
        return f"Заказ {self.id} от {self.created_at}"

    def total_price(self):
        from catalog.models import Product  # Отложенный импорт
        return sum(item.total_price() for item in self.order_items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)  # Используем строковый аргумент, чтобы избежать кругового импорта
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"