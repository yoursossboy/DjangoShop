from rest_framework import serializers
from .models import Product

class ProductModelSerializer(serializers.ModelSerializer):

    category_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category_name']

    def get_category_name(self, obj):
        return obj.category.name