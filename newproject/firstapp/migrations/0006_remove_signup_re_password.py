# Generated by Django 5.0.6 on 2024-06-13 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0005_signup_password_signup_re_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signup',
            name='re_password',
        ),
    ]
