from django.shortcuts import render

# Create your views here.
import re
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import cart,CustomUser
from django.contrib.auth.models import User
from products.models import products,shopping_products
from products.serializers import productsSerializer
from django.core.exceptions import ObjectDoesNotExist

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully.'}, status=201)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user:
        token,_= Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=200)
    return Response({'error': 'Invalid credentials'}, status=401)

class DataAPIView(APIView):#returning user info
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if request.auth:
            
            User=get_user_model()
            user = User.objects.get(id=request.user.id)
            serializer = UserSerializer(user)
            serialized_data = serializer.data


            name=serialized_data['first_name']
            lastname=serialized_data['last_name']
            cart=serialized_data['cart']
        return Response({'name': name, 'lastname':lastname, 'cart':cart})


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([TokenAuthentication])
def add_item(request):#adding items to the cart
    quantity = request.data.get('quantity')
    product_id = request.data.get('pid')
    
    User = get_user_model()
    user = User.objects.get(id=request.user.id)
    
    if user.cart:
        obj=user.cart
        
    else:
        obj = cart()
        obj.save()
        user.cart = obj  # Assign the cart object directly to the user's cart field
        user.save()
    try:
        shopping_product=user.cart.picked_products.get(pid=products.objects.get(id=product_id).pid)
    except ObjectDoesNotExist:
    # Object not found, skip to next line of code
        shopping_product=shopping_products()
    if(user.cart.picked_products.filter(id=shopping_product.id).exists()==False):#if the item isn't already in user's cart
        product=products.objects.get(id=product_id)
        shopping_product=shopping_products.objects.create(title=product.title, price=product.price, shop=product.shop, category=product.category, pid=product.pid,quantity=quantity,product_id=product_id)
        obj.picked_products.add(shopping_product)
        obj.picked_products.get(id=shopping_product.id).quantity+= int(quantity)
        obj.save()
    else:
        temp=obj.picked_products.get(id=shopping_product.id).quantity+ int(quantity)
        obj.picked_products.filter(id=shopping_product.id).update(quantity=temp)
        obj.save()
    obj.quantity += int(quantity)
    obj.save()
    

    
    # Calculate the total price
    picked_products = obj.picked_products.get(id=shopping_product.id)
    total_price = 0
    # for product in picked_products:
    value_without_comma = picked_products.price.replace(',', '') 
    value_without_comma = value_without_comma.replace('.00', '')
    numeric_value = ''.join(filter(str.isdigit, value_without_comma))  
    price = int(numeric_value) 
    total_price += price

    obj.total_price += total_price
    obj.save()

    return Response(status=200)

@api_view(['DELETE'])
@permission_classes([AllowAny])
@authentication_classes([TokenAuthentication])
def delete_all_items(request):
    User=get_user_model()
    user = User.objects.get(id=request.user.id)
    user.cart.delete()
    return Response(status=200)
    
@api_view(['DELETE'])
@permission_classes([AllowAny])
@authentication_classes([TokenAuthentication])
def delete_specific_items(request,pid):

    
    
    User=get_user_model()
    user = User.objects.get(id=request.user.id)
    #calculating how much product removal affects the cart's total bill
    shopping_product=user.cart.picked_products.get(pid=products.objects.get(id=pid).pid)
    user.cart.quantity-=user.cart.picked_products.get(id=shopping_product.id).quantity
    value_without_comma = user.cart.picked_products.get(id=shopping_product.id).price.replace(',', '') 
    value_without_comma = value_without_comma.replace('.00', '')
    numeric_value = ''.join(filter(str.isdigit, value_without_comma))  
    price = int(numeric_value)
    deleted_price=user.cart.picked_products.get(id=shopping_product.id).quantity*price
    user.cart.total_price-=deleted_price

    products_to_remove = shopping_products.objects.filter(id=shopping_product.id)
    for product in products_to_remove:
        user.cart.picked_products.remove(product)
    user.cart.save()
    return Response(status=200)

 
@api_view(['PUT'])
@permission_classes([AllowAny])
@authentication_classes([TokenAuthentication])
def change_product_count(request):
    User=get_user_model()
    user = User.objects.get(id=request.user.id)
    quantity = request.data.get('quantity')
    product_id = request.data.get('pid')


    value_without_comma = user.cart.picked_products.get(product_id=product_id).price.replace(',', '') 
    value_without_comma = value_without_comma.replace('.00', '')
    numeric_value = ''.join(filter(str.isdigit, value_without_comma))  
    price = int(numeric_value)
    obj=user.cart
    obj.total_price-=shopping_products.objects.get(product_id=product_id).quantity*price#fix
    obj.quantity-=shopping_products.objects.get(product_id=product_id).quantity
    obj.save()
    obj.picked_products.filter(product_id=product_id).update(quantity=quantity)
    obj.save()
    total_price=obj.picked_products.get(product_id=product_id).quantity*price
    obj.total_price+=total_price
    total_quantity=obj.picked_products.get(product_id=product_id).quantity
    obj.quantity+=total_quantity
    obj.save()
    return Response(status=200)





