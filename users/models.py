from django.db import models
from products.models import products, shopping_products
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete
from django.dispatch import receiver
class cart(models.Model):
    picked_products=models.ManyToManyField(shopping_products)
    total_price=models.BigIntegerField(default=0)
    quantity=models.IntegerField(default=0)
@receiver(post_delete, sender=cart)
def post_delete_model(sender, instance, **kwargs):
    shopping_products.objects.all().delete()

class CustomUser(AbstractUser):#modifying default user model to include cart
    cart=models.OneToOneField(cart, on_delete=models.SET_DEFAULT, null=True, blank=True,default=None)
