from django.urls import path, include
from .views import list,single,sorted_list
from rest_framework import routers

urlpatterns = [
    path('<str:category>/', list),
    path('<str:category>/sort/<str:sort_by>/', sorted_list),
    path('<str:category>/<int:id>/', single, name='products-detail'),
]