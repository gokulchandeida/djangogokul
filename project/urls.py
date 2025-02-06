"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('register/',views.register, name= 'register'),
    path('login/',views.login_page, name='login'),
    path('logout',views.logout),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:username>/<str:token>/', views.reset_password, name='reset_password'),
    path('my-account',views.profilepage),
    path('admin-account',views.adminpage),
    path('shoplist',views.shoplist, name='shoplist'),
    path('contact',views.contactpage,name='contact'),
    path('viewproduct', views.viewproduct, name='viewproduct'),
    path('addproduct',views.addproductpage,name='addproduct'),
    path('productadminview/<int:product_id>',views.productadminview, name='productadminview'),
    path('addwishlist/<int:d>/', views.addwishlist, name='addwishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove_wishlist/<int:d>/', views.remove_wishlist, name='remove_wishlist'),

    path('single-product/<int:product_id>',views.productdetail, name='single-product'),

    path('basic-phones',views.basicphones, name='basic-phones'),
    path('smart-phones',views.smartphones, name='smart-phones'),
    path('wifi-tablets',views.wifitablet, name='wifi-tablets'),
    path('sim-tablet',views.simtablet, name='sim-tablet'),
    path('pos-tablet',views.postablet, name='pos-tablet'),
    path('laptop',views.laptop, name='laptop'),
    path('desktop',views.desktop, name='desktop'),
    path('all-in-one',views.allinone, name='all-in-one'),
    path('servers',views.server, name='servers'),
    path('standard-tv',views.standardtv, name='standard-tv'),

    path('smart-tv',views.smarttv, name='smart-tv'),
    path('headphones',views.headphones, name='headphones'),
    path('speakers',views.speakers, name='speakers'),
    path('amplifiers',views.amplifiers, name='amplifiers'),
    path('wearables',views.wearable, name='wearables'),
    path('smart-office',views.smartoffice, name='smart-office'),
    path('smart-home',views.smarthome, name='smart-home'),
    path('security',views.security, name='security'),
    path('mobile-chargers',views.mobilecharger, name='mobile-chargers'),
    path('mobile-screen-guards',views.screenguard, name='mobile-screen-guards'),   

    path('mobile-covers',views.mobilecover, name='mobile-covers'),
    path('battery-bank',views.batterybank, name='battery-bank'),
    path('mobile-headset',views.headset, name='mobile-headset'),
    path('selfie-stick',views.selfiestick, name='selfie-stick'),
    path('tablet-covers',views.tabletcover, name='tablet-covers'),
    path('tablet-stand',views.tabletstand, name='tablet-stand'),
    path('stylus-pen',views.styluspen, name='stylus-pen'),
    path('tablet-screen-guard',views.tabletscreenguard, name='tablet-screen-guard'),
    path('data-card',views.datacard, name='data-card'),
    path('tablet-keyboards',views.tabletkeyboard, name='tablet-keyboards'),

    path('chargers-cables-pc',views.pccables, name='chargers-cables-pc'),
    path('keyboards',views.keyboard, name='keyboards'),
    path('mouse',views.mouse, name='mouse'),
    path('hubs-ports',views.hubs, name='hubs-ports'),
    path('webcam',views.webcam, name='webcam'),
    path('ups',views.ups, name='ups'),
    path('monitor',views.monitor, name='monitor'),
    path('hard-disk',views.harddisk, name='hard-disk'),
    path('graphics-card',views.graphicscard, name='graphics-card'),
    path('components',views.components, name='components'),       
    path('wifi-routers',views.wifirouter, name='wifi-routers'),
    path('printers',views.printer, name='printers'),    

    path('updateproduct',views.updateproductpage),
    path('updateproduct/update/<d>',views.updateproductpage),
    path('updateproduct/delete/<s>',views.dele),
    path('cart/<s>',views.cart,name='cart'),
    path('cart_dis',views.cart_dis,name='cart_dis'),
    path('delete/<str:item_name>', views.delete_item, name='delete'),
    path('remove/<str:product_name>',views.remove_cart),

    path('cart_dis/remove/<str:product_name>/', views.cart_remove, name='cart_remove'),
    path('increment/<str:product_name>/', views.cart_increment, name='cart_increment'),
    path('decrement/<str:product_name>/', views.cart_decrement, name='cart_decrement'),
    path('orders/', views.order_details, name='orders'),
    path('checkout',views.checkout,name='checkout'),
    path('payment/success/',views.process_payment, name='process_payment'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

