# Generated by Django 5.1.2 on 2024-10-27 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='products_detail',
            new_name='product_data',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='user_details',
            new_name='user_data',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='total_price',
        ),
    ]
