from rest_framework import serializers
from .models import Product


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'code', 'price',
                  'category', 'slug', 'description', 'additional_info', 'image1')
