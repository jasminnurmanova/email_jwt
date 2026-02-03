from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from accounts.models import CartItem,Cart
from products.serializers import ProductSerializer


class SignUpSerializer(serializers.ModelSerializer):
    confirm_pass = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'password', 'confirm_pass']
        
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_pass = attrs.get('confirm_pass')
        if password is None or confirm_pass is None or password != confirm_pass:
            raise ValidationError({"success": False, 'message': 'Parollar toliq kiritilmagan'})
        
        return attrs
        
    def create(self, validated_data):
        validated_data.pop('confirm_pass')
        user = User.objects.create_user(**validated_data)
        # user.set_password(validated_data['password'])
        # user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True,required=True)
    new_password=serializers.CharField(write_only=True,required=True)

    def validate_old_password(self,value):
        user=self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def validate_new_password(self,value):
        validate_password(value)
        return value

    def save(self,**kwargs):
        user=self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class CartItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)

    class Meta:
        model=CartItem
        fields=("id","product","quantity")


class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True)

    class Meta:
        model=Cart
        fields=("id","items")








    


    