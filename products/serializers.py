from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'created_at']



class ProductCreateSerializer(serializers.ModelSerializer):

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    class Meta:
        model = Product
        fields = ['title', 'description', 'price']