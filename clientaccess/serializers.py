from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Item, Order, ShoppingCart

class BasicItemSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Item 
        fields = ['id', 'name', 'price']

class ItemSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Item 
        fields = ['id', 'name', 'price', 'details']

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'password', 'email']

class OrderSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Order
        fields = ['order_id', 'user_id', 'item_id', 'quantity', 'order_date', 'deliver_date']

class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ShoppingCart 
        fields = ['user_id', 'item_id', 'quantity']


