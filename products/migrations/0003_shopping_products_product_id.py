# Generated by Django 4.2.1 on 2023-06-02 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_shopping_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopping_products',
            name='product_id',
            field=models.CharField(default=None, max_length=10),
        ),
    ]