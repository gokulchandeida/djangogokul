# Generated by Django 5.1.2 on 2024-10-27 13:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_addproduct_image_alter_updateproduct_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('total_price', models.IntegerField(default=0)),
                ('products_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.addproduct')),
                ('user_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.signup')),
            ],
        ),
    ]
