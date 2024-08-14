
import django
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import*





class signup(models.Model):
    username=models.CharField(max_length=200)
    your_email=models.EmailField()
    password=models.CharField(max_length=20)
    # re_password=models.CharField(max_length=20, default='password')

class signinn(models.Model):
    myname=models.CharField(max_length=200)
    mypass=models.CharField(max_length=20)
  
class addproduct(models.Model):
    productname=models.CharField(max_length=200)
    productcat=models.CharField(max_length=150)
    productdes=models.CharField(max_length=2000)
    productinfo=models.CharField(max_length=2000)
    productsize=models.CharField(max_length=100)
    productcolor=models.CharField(max_length=150)
    discountprice=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    productimg=models.FileField()
   

    def __str__(self):
       return self.productname
    
class updateproduct(models.Model):

    productname=models.CharField(max_length=200)
    productcat=models.CharField(max_length=150)
    productdes=models.CharField(max_length=2000)
    productinfo=models.CharField(max_length=2000)
    productsize=models.CharField(max_length=10)
    productcolor=models.CharField(max_length=150)
    discountprice=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    productimg=models.FileField()

    def __str__(self):
       return self.productname


class sampleforms(models.Model):
    rollno=models.IntegerField()
    name=models.CharField(max_length=50)
    age=models.IntegerField()  

class cartitems(models.Model):
    user_data=models.ForeignKey(signup,on_delete=models.CASCADE)
    product_data=models.ForeignKey(addproduct,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    total_price=models.FloatField(default=0)
   
