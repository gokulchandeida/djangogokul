# Generated by Django 5.1.2 on 2025-01-24 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_wishlist_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='internationalshipping',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AlterField(
            model_name='order',
            name='billing_address',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.CharField(max_length=500),
        ),
        migrations.DeleteModel(
            name='ProductComparison',
        ),
    ]
