from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import Http404
from rest_framework import status,viewsets
from rest_framework import permissions
from rest_framework import generics
from .models import products
from django.core.serializers import serialize   
from .serializers import productsSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, renderer_classes,permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.reverse import reverse,reverse_lazy

@api_view()
@permission_classes([IsAuthenticatedOrReadOnly])
def list(request, category):
    queryset=products.objects.all().filter(category=category)
    serializer = productsSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@api_view()
@permission_classes([IsAuthenticatedOrReadOnly])
def sorted_list(request, category,sort_by):
    queryset=products.objects.all().filter(category=category)
    if sort_by=="l2h":
        queryset=queryset.order_by("price")
    elif sort_by=="h2l":
        queryset=queryset.order_by("-price")
    serializer = productsSerializer(queryset, many=True, context={'request': request}) 
    return Response(serializer.data)

@api_view()
@permission_classes([IsAuthenticatedOrReadOnly])
def single(request, category,id):
    if(products.objects.filter(category=category).exists()):
        queryset=products.objects.get(id=id)
        serializer = productsSerializer(queryset, context={'request': request})
        return Response(serializer.data)
    raise Http404("Object not found")









