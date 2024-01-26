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
from .serializers import UserSerializer, ItemSerializer, ShoppingCartSerializer, OrderSerializer

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
def list_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'Item': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['GET'])
def all_items(request):
    queryset = Item.objects.all()
    serializer = ItemSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    serializer = ShoppingCartSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'Item': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAdminUser])
def all_carts(request):
    queryset = ShoppingCart.objects.all()
    serializer = ShoppingCartSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def my_cart(request):
    user_id = request.data["user"]
    queryset = ShoppingCart.objects.all().filter(user=user_id)
    serializer = ShoppingCartSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_item(request):
    user_id = request.data["user"]
    entry_id = request.data["id"]
    ShoppingCart.objects.all().filter(user=user_id).filter(id=entry_id).delete()
    return Response({"message":"Succesfully removed"})

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def order(request):
    user = get_object_or_404(ShoppingCart, user=request.data['user'])
    user_id = request.data["user"]
    queryset = ShoppingCart.objects.all().filter(user=user_id)
    items = []
    for item in queryset:
        items.append(item.item)
    data = request.data
    data["items"] = str(items)
    data["deliver_date"] = datetime.datetime.strptime(data["deliver_date"], "%Y-%m-%d").date()
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'Item': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)