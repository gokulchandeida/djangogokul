"""
URL configuration for newproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from firstapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home), 
    path('signup',views.register), 
    path('home',views.sub),
    path('login',views.signin), 
    path('admin',views.adminpage),
    path('addproducts',views.addproductpage),
    path('viewproducts',views.viewproductpage),
    path('detail/<d>',views.productdetailpage),
    
    path('support',views.supportpage),
    path('profile',views.profilepage),
    path('shop',views.shoppage),
    path('updateproduct',views.updateproductpage),
    path('updateproduct/update/<d>',views.updateproductpage),
    path('updateproduct/delete/<s>',views.dele),
    path('logout',views.logout),
    #path('cartitems',views.cartsummary),
    #path('cart/create/<int:product_id>/', views.cartsummary, name='add_to_cart'),
    #path('cart/', views.cartdisplay, name='cartdisplay'),
    #path('cartsummary/remove/<int:cart_item_id>/', views.removecart, name='removecart'),
    path('userregister',views.userform),
    path('userpro',views.user_profile),
    path('cart/<s>',views.cart),
    path('cart_dis',views.cart_dis),
    path('remove/<t>',views.cart_remove)
    
 ]  


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
