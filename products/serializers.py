from rest_framework import serializers
from .models import products, shopping_products
from rest_framework.reverse import reverse,reverse_lazy
class productsSerializer(serializers.ModelSerializer):
    class Meta:
        model = products
        fields = '__all__'
    def to_representation(self, instance):
        request = self.context.get('request')
        url = reverse('products-detail', kwargs={'id': instance.id, 'category': instance.category}, request=request)#url to the instance
        representation = super().to_representation(instance)
        representation['url']=url
        return representation
    
class shopping_productsSerializer(serializers.ModelSerializer):
    class Meta:
        model = shopping_products
        fields = '__all__'
