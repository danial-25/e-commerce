# Generated by Django 4.2.1 on 2023-06-01 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='shopping_products',
            fields=[
                ('products_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.products')),
                ('quantity', models.IntegerField(default=0)),
            ],
            bases=('products.products',),
        ),
    ]
