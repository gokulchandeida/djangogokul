# Generated by Django 5.0.6 on 2024-06-14 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0006_remove_signup_re_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='signinn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myname', models.CharField(max_length=200)),
                ('your_pass', models.CharField(max_length=20)),
            ],
        ),
        migrations.RenameField(
            model_name='signup',
            old_name='your_name',
            new_name='username',
        ),
    ]