# Generated by Django 5.0.6 on 2024-06-21 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0009_rename_your_pass_signinn_mypass'),
    ]

    operations = [
        migrations.CreateModel(
            name='addproduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productname', models.CharField(max_length=200)),
                ('productcat', models.CharField(max_length=150)),
                ('productdes', models.CharField(max_length=1000)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
    ]