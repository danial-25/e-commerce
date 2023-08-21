# Generated by Django 4.2.1 on 2023-05-26 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_customuser_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cart',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='users.cart'),
        ),
    ]
