import django
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

# User Registeration

class signup(models.Model):
    username=models.CharField(max_length=20)
    useremail=models.EmailField()
    userpassword=models.CharField(max_length=20)
# User Signin
class signinn(models.Model):
    username=models.CharField(max_length=200)
    userpassword=models.CharField(max_length=20)


# Add Products
class addproduct(models.Model):
    name=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    description=models.CharField(max_length=2000)
    information=models.CharField(max_length=2000)
    sku=models.CharField(max_length=100, unique=True)
    color=models.CharField(max_length=150)
    tag1=models.CharField(max_length=150)
    tag2=models.CharField(max_length=150)
    tag3=models.CharField(max_length=150)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=0.0,null=True)
    image=models.ImageField()    
  
    def __str__(self):
       return self.name

#Edit Product

class updateproduct(models.Model):
    name=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    description=models.CharField(max_length=2000)
    information=models.CharField(max_length=2000)
    sku=models.CharField(max_length=100, unique=True)
    color=models.CharField(max_length=150)
    tag1=models.CharField(max_length=150)
    tag2=models.CharField(max_length=150)
    tag3=models.CharField(max_length=150)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=0.0, null=True)
    image=models.ImageField()

    def __str__(self):
       return self.name

# add cart

class Cart(models.Model):
    user_data=models.ForeignKey(signup,on_delete=models.CASCADE)
    product_data=models.ForeignKey(addproduct,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
   
    def item_total(self):
        return self.product_data.price * self.quantity
    def total_price(self):
        return self.product_data.price * self.quantity



class Order(models.Model):
    user_data = models.ForeignKey(signup, on_delete=models.CASCADE)
    product_data = models.ForeignKey(addproduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    billing_name = models.CharField(max_length=100)
    billing_address = models.CharField(max_length=500)
    shipping_name = models.CharField(max_length=100)
    shipping_address = models.CharField(max_length=500)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} for {self.user_data.username}"
    
class Wishlist(models.Model):
    user = models.ForeignKey(signup, on_delete=models.CASCADE)
    product = models.ForeignKey(addproduct, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"Wishlist of {self.user.username} - {self.product.name}"
  






