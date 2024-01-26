from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Item, Order, ShoppingCart

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
        fields = ['id', 'user', 'items', 'order_date', 'deliver_date']

class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ShoppingCart 
        fields = ['id', 'user', 'item']


