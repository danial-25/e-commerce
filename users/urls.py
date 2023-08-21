from django.urls import path
from .views import UserRegistrationView, user_login,DataAPIView,add_item,delete_all_items,delete_specific_items,change_product_count

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', user_login, name='user-login'),
    path('data/', DataAPIView.as_view()),
    path('add_item/', add_item),
    path('cart/delete/', delete_all_items),
    path('cart/delete/<int:pid>/',delete_specific_items),
    path('cart/change/', change_product_count),

]