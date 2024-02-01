from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Item, Order, ShoppingCart
import datetime

# Create your views here.
from .serializers import UserSerializer, ItemSerializer, ShoppingCartSerializer, OrderSerializer, BasicItemSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAdminUser])
def add_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'Item': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['GET'])
def all_items(request):
    try:
        queryset = Item.objects.all()
        serializer = BasicItemSerializer(queryset, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def see_item(request):
    try:
        item_id = request.GET.get('itemid', '')
        queryset = Item.objects.all().filter(id=item_id)
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT','PATCH'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    if request.method == 'PATCH':
        try:
            entry_to_update = ShoppingCart.objects.get(item_id=request.data["item_id"], user_id= request.data["user_id"])
        except ShoppingCart.DoesNotExist:
            return Response({"detail": "Particular item is not in user's cart"}, status=status.HTTP_404_NOT_FOUND)
        old_quantity = entry_to_update.quantity
        new_quantity = old_quantity+1
        entry_to_update.quantity = new_quantity
        serializer = ShoppingCartSerializer(data=request.data)
        if serializer.is_valid():
            entry_to_update.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        if ShoppingCart.objects.filter(item_id=request.data["item_id"], user_id= request.data["user_id"]).exists():
            return Response({"detail": "Item already exists in the cart"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        serializer = ShoppingCartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Item': serializer.data})
        return Response(serializer.errors, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def my_cart(request):
    try:
        user_id = request.GET.get('userid', '')
        queryset = ShoppingCart.objects.all().filter(user_id=user_id)
        serializer = ShoppingCartSerializer(queryset, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE', 'PATCH'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    if request.method == 'PATCH':
        try:
            entry_to_update = ShoppingCart.objects.get(item_id=request.data["item_id"], user_id= request.data["user_id"])
        except ShoppingCart.DoesNotExist:
            return Response({"detail": "Particular item is not in user's cart"}, status=status.HTTP_404_NOT_FOUND)
        old_quantity = entry_to_update.quantity
        new_quantity = old_quantity-1
        if new_quantity==0:
            return Response({"detail": "There were no multiple items in cart"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        entry_to_update.quantity = new_quantity
        entry_to_update.save()
        serializer = ShoppingCartSerializer(entry_to_update)
        return Response(serializer.data)
    elif request.method == 'DELETE':
            try:
                obj_to_delete = ShoppingCart.objects.get(item_id=request.data["item_id"], user_id= request.data["user_id"])
            except ShoppingCart.DoesNotExist:
                return Response({"detail": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
            obj_to_delete.delete()
            return Response({"detail": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def order(request):
    usercart = ShoppingCart.objects.filter(user_id= request.data["user_id"])
    if not usercart.exists():
        return Response({"detail": "User do not have items in cart"}, status=status.HTTP_404_NOT_FOUND)
    shopping_cart_serializer = ShoppingCartSerializer(data=usercart, many=True)
    shopping_cart_serializer.is_valid()
    order_entries = []
    for order_entry in shopping_cart_serializer.data:
        order_entry["deliver_date"] = datetime.datetime.strptime(request.data["deliver_date"], "%Y-%m-%d").date()
        order_entry["order_id"] = request.data["order_id"]
        order_entries.append(order_entry)
    serializer = OrderSerializer(data=order_entries, many=True)
    if serializer.is_valid():
        serializer.save()
        usercart.delete()
        return Response({'Item': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)