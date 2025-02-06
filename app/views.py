import json
from .models import *
from django.conf import settings
from django.http import HttpResponse
import pytz
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.tokens import default_token_generator
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse

from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.core.paginator import Paginator


# Create your views here.

# hompage display
def home(request):
   return render(request,"index.html")

# user login
def login_page(request):
   if request.method== "POST":
        x=request.POST["username"]
        y=request.POST["userpassword"]
        try:
            data=signup.objects.get(username=x)
            if y==data.userpassword:
                request.session['user']=x
                request.session.set_expiry(86400)
                return render(request,"my-account.html")
            else:
                return render(request,"index.html")
        except Exception:
            if x=="admin" and y=="admin":
                request.session['admin']=x
                request.session.set_expiry(86400)
                return render(request,"admin-account.html")
            else:
                messages.error(request,"Error Invalid Admin")

   return render(request,"login.html")

# user registration
def register(request):

    if request.method== "POST":
        a=request.POST["username"]
        b=request.POST["useremail"]
        c=request.POST["userpassword"]
        try:
            k=signup.objects.get(username=a)
            print(k.username)
            if k is not None:
                messages.error(request,'already exits')
        except:
            myuser=signup.objects.create(username=a,useremail=b,userpassword=c)
            myuser.save()
    return render(request,"login.html")

# user logout

def logout(re):
    if 'user' in re.session or 'admin' in re.session:
        re.session.flush()
        return redirect(login_page)

# user dashboard
def profilepage(re):
    return render(re,"my-account.html")

# admin dashboard
def adminpage(re):
    return render(re,"admin-account.html")
# add products
def contactpage(re):
    return render(re,"contact.html")
def addproductpage(request):
    if 'admin' in request.session:
        if request.method == "POST":
            a = request.POST.get("name")
            b = request.POST.get("category")
            c = request.POST.get("description")
            d = request.POST.get("information")
            e = request.POST.get("sku")
            f = request.FILES.get("image")
            g = request.POST.get("color")
            h = request.POST.get("tag1")
            i = request.POST.get("tag2")
            j = request.POST.get("tag3")
            k = request.POST.get("price")

            if not k or k == '':
                return render(request, "addproduct.html", {"error": "Price is required."})

            try:
                k = float(k)
            except ValueError:
                return render(request, "addproduct.html", {"error": "Invalid price format."})

            # SKU check
            if addproduct.objects.filter(sku=e).exists():
                return render(request, "addproduct.html", {"error": "SKU already exists. Please use a different SKU."})

            myprod = addproduct.objects.create(
                name=a,
                category=b,
                description=c,
                information=d,
                sku=e,
                image=f,
                color=g,
                tag1=h,
                tag2=i,
                tag3=j,
                price=k
            )
            myprod.save()
        # Sorting logic
        sort_by = request.GET.get('sort_by', 'name')  
        order = request.GET.get('order', 'asc')  

        order_prefix = '' if order == 'asc' else '-'

        
        if sort_by == 'price':
            product_list = addproduct.objects.all().order_by(f'{order_prefix}price')
        elif sort_by == 'category':
            product_list = addproduct.objects.all().order_by(f'{order_prefix}category')
        else:
            product_list = addproduct.objects.all().order_by(f'{order_prefix}name')
      
        # Pagination
        paginator = Paginator(product_list, 9)  # Showd 9 products
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "addproduct.html", {
            "d": page_obj,
            "product_count": page_obj.paginator.count,
            "total_products": paginator.count,
            "sort_by": sort_by,
            "order": order
        })

    return render(request, "login.html")  



def shoplist(request):
    # get all products
    data=addproduct.objects.all()
    products = addproduct.objects.all()

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  #  9 products per page
    page_number = request.GET.get('page')  # current page number 
    page_obj = paginator.get_page(page_number)

    return render(request, "shoplist.html", {"page_obj": page_obj,"d":data})

def basicphones(request):

    products = addproduct.objects.filter(category='Basic Phones')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "basic-phones.html", {"page_obj": page_obj})

def smartphones(request):
   
    products = addproduct.objects.filter(category='Smart Phones')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "smart-phones.html", {"page_obj": page_obj})

def wifitablet(request):
 
    products = addproduct.objects.filter(category='Wifi Tablet')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "wifi-tablets.html", {"page_obj": page_obj})

def simtablet(request):
   
    products = addproduct.objects.filter(category='Sim Tablet')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "sim-tablet.html", {"page_obj": page_obj})

def postablet(request):

    products = addproduct.objects.filter(category='POS Tablet')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "pos-tablet.html", {"page_obj": page_obj})

def laptop(request):
   
    products = addproduct.objects.filter(category='Laptop')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "laptop.html", {"page_obj": page_obj})

def desktop(request):
  
    products = addproduct.objects.filter(category='Desktop')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "desktop.html", {"page_obj": page_obj})

def server(request):
   
    products = addproduct.objects.filter(category='Server')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "servers.html", {"page_obj": page_obj})

def allinone(request):

    products = addproduct.objects.filter(category='All in One')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "all-in-one.html", {"page_obj": page_obj})

def standardtv(request):
   
    products = addproduct.objects.filter(category='Standard TV')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "standard-tv.html", {"page_obj": page_obj})

def smarttv(request):

    products = addproduct.objects.filter(category='Smart TV')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "smart-tv.html", {"page_obj": page_obj})

def headphones(request):
   
    products = addproduct.objects.filter(category='Head Phones')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "headphones.html", {"page_obj": page_obj})

def speakers(request):

    products = addproduct.objects.filter(category='Speakers')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "speakers.html", {"page_obj": page_obj})

def amplifiers(request):
   
    products = addproduct.objects.filter(category='Amplifiers')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "amplifiers.html", {"page_obj": page_obj})

def security(request):

    products = addproduct.objects.filter(category='Security')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "security.html", {"page_obj": page_obj})

def smartoffice(request):
   
    products = addproduct.objects.filter(category='Smart Office')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "smart-office.html", {"page_obj": page_obj})

def wearable(request):
    
    products = addproduct.objects.filter(category='Wearable')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "wearables.html", {"page_obj": page_obj})

def smarthome(request):
   
    products = addproduct.objects.filter(category='Smart Home')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "smart-home.html", {"page_obj": page_obj})

def mobilecharger(request):
    
    products = addproduct.objects.filter(category='Mobile Charger')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "mobile-chargers.html", {"page_obj": page_obj})

def screenguard(request):
   
    products = addproduct.objects.filter(category='Screen Guard')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "mobile-screen-guards.html", {"page_obj": page_obj})

def selfiestick(request):
    
    products = addproduct.objects.filter(category='Selfie Stick')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "selfie-stick.html", {"page_obj": page_obj})

def mobilecover(request):
   
    products = addproduct.objects.filter(category='Mobile Cover')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "mobile-covers.html", {"page_obj": page_obj})

def batterybank(request):

    products = addproduct.objects.filter(category='Battery Bank')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "battery-bank.html", {"page_obj": page_obj})

def datacard(request):
   
    products = addproduct.objects.filter(category='Data Card')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "data-card.html", {"page_obj": page_obj})

def tabletcover(request):
    
    products = addproduct.objects.filter(category='Tablet Cover')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "tablet-covers.html", {"page_obj": page_obj})

def tabletkeyboard(request):
   
    products = addproduct.objects.filter(category='Tablet Keyboard')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "tablet-keyboards.html", {"page_obj": page_obj})

def tabletstand(request):
    
    products = addproduct.objects.filter(category='Tablet Stand')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "tablet-stand.html", {"page_obj": page_obj})

def tabletscreenguard(request):
   
    products = addproduct.objects.filter(category='Tablet Screen Guard')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "tablet-screen-guard.html", {"page_obj": page_obj})

def styluspen(request):
    
    products = addproduct.objects.filter(category='Stylus Pen')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "stylus-pen.html", {"page_obj": page_obj})

def headset(request):
   
    products = addproduct.objects.filter(category='Headset')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "mobile-headset.html", {"page_obj": page_obj})

def harddisk(request):
    
    products = addproduct.objects.filter(category='Hard Disk')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "hard-disk.html", {"page_obj": page_obj})

def monitor(request):
   
    products = addproduct.objects.filter(category='Monitor')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "monitor.html", {"page_obj": page_obj})

def graphicscard(request):
    #  category 'Basic Phones'
    products = addproduct.objects.filter(category='Graphics')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "graphics-card.html", {"page_obj": page_obj})

def components(request):
   
    products = addproduct.objects.filter(category='Components')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "components.html", {"page_obj": page_obj})

def printer(request):
    
    products = addproduct.objects.filter(category='Printer')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "printers.html", {"page_obj": page_obj})

def wifirouter(request):
   
    products = addproduct.objects.filter(category='Router')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "wifi-routers.html", {"page_obj": page_obj})

def ups(request):
    
    products = addproduct.objects.filter(category='UPS')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "ups.html", {"page_obj": page_obj})

def webcam(request):
   
    products = addproduct.objects.filter(category='Webcam')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "webcam.html", {"page_obj": page_obj})


def pccables(request):
    
    products = addproduct.objects.filter(category='Cables')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "chargers-cables-pc.html", {"page_obj": page_obj})

def hubs(request):
   
    products = addproduct.objects.filter(category='Hub')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "hubs-ports.html", {"page_obj": page_obj})

def mouse(request):
    
    products = addproduct.objects.filter(category='Mouse')

    
    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, "mouse.html", {"page_obj": page_obj})

def keyboard(request):
   
    products = addproduct.objects.filter(category='Keyboard')

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, "keyboards.html", {"page_obj": page_obj})

def updateproductpage(request,d):
    if request.method== "POST":
            a1=request.POST["name"]
            b1=request.POST["category"]
            c1=request.post["description"]
            d1=request.POST["information"]
            e1=request.POST["sku"]
            f1=request.FILES["image"]
            g1=request.POST["color"]
            h1=request.POST["tag1"]
            i1=request.POST["tag2"]
            j1=request.POST["tag3"]
            k1=request.POST["price"]
        
            addproduct.objects.filter(name=a1).update(category=b1,description=c1,information=d1,sku=e1,image=f1,color=g1,tag1=h1,tag2=i1,tag3=j1,price=k1)
            messages.success(request,'Product Updated Sucessfully')
            return redirect(shoplist)
    data=addproduct.objects.get(pk=d)
    return render(request,"updateproduct.html",{"d":data})

# delete products

def dele(re,s):
    l=addproduct.objects.get(pk=s)
    l.delete()
    messages.success(re,"Deleted")
    return redirect(shoplist)
# Sample viewproducts

def viewproduct(request):
    data=addproduct.objects.all()
    products = addproduct.objects.all()

    sort_by = request.GET.get('sort', '')  

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 9)  #  9 products per page
    page_number = request.GET.get('page')  # current page number 
    page_obj = paginator.get_page(page_number)

    return render(request, "viewproduct.html", {"page_obj": page_obj,"d":data})


def productdetail(request, product_id):
    product = addproduct.objects.get(pk=product_id)
    
    # Get the current user's cart data for this product
    if 'user' in request.session:
        data = signup.objects.get(username=request.session['user'])
        cart_items = Cart.objects.filter(user_data=data)
        
        grouped_items = {}
        for item in cart_items:
            product_name = item.product_data.name
            quantity = item.quantity
            
            if product_name in grouped_items:
                grouped_items[product_name]['quantity'] += quantity
            else:
                grouped_items[product_name] = {
                    'quantity': quantity,
                    'product_data': item.product_data
                }
        
        # Check if the current product is in the cart
        product_in_cart = grouped_items.get(product.name, None)
    else:
        product_in_cart = None
        
    related_products = addproduct.objects.filter(category=product.category).exclude(pk=product.id)[:4]  # Limit to 4 products

    return render(request, 'single-product.html', {
        'product': product,
        'product_in_cart': product_in_cart,
        'related_products': related_products  
    })

# def productdetail(request, product_id):
#     product = addproduct.objects.get(pk=product_id)
#     selected_quantity = int(request.GET.get('quantity', 1))
#     quantities = range(1, 11)
    
#     return render(request, 'single-product.html', {
#         'product': product,
#         'quantities': quantities,
#         'selected_quantity': selected_quantity, 
#     })


# def productdetailpage(request,c):
#     # product = get_object_or_404(addproduct, pk=c)
#     product=addproduct.objects.get(pk=c)
#     product_in_cart = False
#     if 'cart' in request.session:
#         cart = request.session['cart']
#         if product.id in cart:
#             product_in_cart = True

#     return render(request,"single-product.html",{
#         'product': product,
#         'product_in_cart': product_in_cart
#         })


def addwishlist(request, d):
    if 'user' in request.session:
        try:
            user = signup.objects.get(username=request.session['user'])
        except signup.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect(login)

        try:
            product = addproduct.objects.get(pk=d)
        except addproduct.DoesNotExist:
            messages.error(request, 'Product does not exist.')
            return redirect(shoplist)

        # Check if the product is already in the wishlist
        if Wishlist.objects.filter(user=user, product=product).exists():
            messages.info(request, 'Product is already in your wishlist.')
        else:
            # Set the time zone to IST
            ist_timezone = pytz.timezone('Asia/Kolkata')
            current_date = timezone.now().astimezone(ist_timezone)
            Wishlist.objects.create(product=product, user=user, added_at=current_date)
            messages.success(request, 'Item Added to Wish List Successfully')
        
        return redirect(wishlist)
    
    return redirect(login)

def wishlist(request):
    if 'user' in request.session:
        user = signup.objects.get(username=request.session['user'])
        wishlist_items = Wishlist.objects.filter(user=user)  # Use `user` here, not `user_details`
        wishlist_count = wishlist_items.count() 
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items, 'wishlist_count': wishlist_count})
    return redirect(shoplist)

def remove_wishlist(request,d):
    try:
        wishlist_item = Wishlist.objects.get(pk=d)
        wishlist_item.delete()
        messages.success(request, 'Item removed from wishlist.')
    except Wishlist.DoesNotExist:
        messages.error(request, 'Item not found in your wishlist.')
    return redirect(wishlist)


# def remove_wishlist(request, product_id):
#     try:
#         wishlist_item = Wishlist.objects.get(user=request.user, product_id=product_id)
#         wishlist_item.delete()
#     except Wishlist.DoesNotExist:
#         pass
#     return redirect('wishlist')

# add to cart

def cart(re,s):
    if 'user' in re.session:
        data=signup.objects.get(username=re.session['user'])
        l=addproduct.objects.get(pk=s)

        user_cart=Cart.objects.create(user_data=data,product_data=l)
        user_cart.save()
        messages.success(re,"successfully")


    return redirect(cart_dis)
# def cart(request, s):
#     if 'user' in request.session:
#         data = signup.objects.get(username=request.session['user'])
#         l = addproduct.objects.get(pk=s)
        
#         # Get quantity from the GET request, default to 1
#         quantity = int(request.GET.get('quantity', 1))
        
#         # Check if the product is already in the cart
#         existing_cart_item = Cart.objects.filter(user_data=data, product_data=l).first()
        
#         if existing_cart_item:
#             # If the product already exists, update the quantity
#             existing_cart_item.quantity = existing_cart_item.quantity + quantity
#             existing_cart_item.save()
#             messages.success(request, "Updated quantity in your cart.")
#         else:
#             # Otherwise, create a new cart entry
#             user_cart = Cart.objects.create(user_data=data, product_data=l, quantity=quantity)
#             user_cart.save()
#             messages.success(request, "Product added to cart successfully.")
        
#         return redirect('cart_dis')
    
#     return redirect('login')  # Redirect if user is not logged in

# def cart(request, s):
#     if 'user' in request.session:
#         data = signup.objects.get(username=request.session['user'])
#         product = addproduct.objects.get(pk=s)

#         # Initialize the cart session if it's not already there
#         if 'cart' not in request.session:
#             request.session['cart'] = []

#         # If the product is not already in the cart, add it
#         if product.name not in request.session['cart']:
#             request.session['cart'].append(product.name)
#             request.session.modified = True
#             messages.success(request, "Product added to cart!")
#         else:
#             messages.info(request, "Product already in the cart!")

#         return redirect('cart_dis')
    
#     return redirect('login')

def disproduct(request):
        all_products = addproduct.objects.all()
        cart_item_ids = []
        if 'user' in request.session:
            user = signup.objects.get(username=request.session['user'])
            cart_items = Cart.objects.filter(user_details=user)
            cart_item_ids = [item.product_data.id for item in cart_items]
        return render(request, 'display-cart.html', {'all_products': all_products, 'cart_item_ids': cart_item_ids})

def cart_dis(request):
    if 'user' in request.session:
        data = signup.objects.get(username=request.session['user'])
        cart_items = Cart.objects.filter(user_data=data)
        # cart_count = cart_items.count()
        cart_count=0
        grouped_items = {}
        total = 0

        for item in cart_items:
            product_name = item.product_data.name
            quantity = item.quantity
            price = item.product_data.price
            product_image = item.product_data.image
            cart_count += quantity


            if product_name in grouped_items:
                grouped_items[product_name]['quantity'] += quantity
                grouped_items[product_name]['total'] += price * quantity
                # item_count += quantity
            else:
                grouped_items[product_name] = {
                    'quantity': quantity,
                    'price': price,
                    'total': price * quantity,
                    'image': product_image,
                    
                    
                }

        sub_total = sum(value['total'] for value in grouped_items.values())
        shipping_cost = 299
        grand_total = sub_total + shipping_cost

        return render(request, 'cart.html', {
            'grouped_items': grouped_items,
            'grand_total': grand_total,
            'shipping_cost': shipping_cost,
            'sub_total': sub_total,
            'cart_count': cart_count,
            
            })
            

    return redirect('login')  # Redirect if user is not logged in

  

def delete_item(request, item_name):
    if 'user' in request.session:
        user_data = signup.objects.get(username=request.session['user'])
        # Ensure we're removing the correct item for the logged-in user
        item_to_remove = Cart.objects.filter(product_data__name=item_name, user_data=user_data).first()
        if item_to_remove:
            item_to_remove.delete()
            messages.success(request, "Item removed successfully")
        else:
            messages.error(request, "Item not found or not owned by you")
        return redirect('cart_dis')  # Ensure this matches the name of your cart view

    return redirect('login')  # Redirect if user is not logged in

def remove_cart(re,d):
    if 'user' in re.session:
        Cart.objects.filter(pk=d).delete()
        messages.success(re,"remove successfully")
        return redirect(cart_dis)
    
def cart_remove(re, product_name):
    if 'user' in re.session:
        data = signup.objects.get(username=re.session['user'])
    
        Cart.objects.filter(user_data=data, product_data__productname=product_name).delete()
        messages.success(re, "Removed all items of '{}' from cart successfully.".format(product_name))
        return redirect('cart_dis')  # Redirect to your cart display view

    return redirect('')  # Redirect if user is not logged in
    

def cart_increment(request, product_name):
    if 'user' in request.session:
        data = signup.objects.get(username=request.session['user'])
        item = Cart.objects.filter(user_data=data, product_data__name=product_name).first()
        
        if item:
            item.quantity += 1
            item.save()
            messages.success(request, f"Increased quantity of '{product_name}' to {item.quantity}.")
        else:
            messages.warning(request, f"Item '{product_name}' not found in cart.")

        return redirect('cart_dis')

    return redirect('login')  # Redirect if user is not logged in

def cart_decrement(request, product_name):
    if 'user' in request.session:
        data = signup.objects.get(username=request.session['user'])
        item = Cart.objects.filter(user_data=data, product_data__name=product_name).first()
        
        if item:
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
                messages.success(request, f"Decreased quantity of '{product_name}' to {item.quantity}.")
            else:
                messages.warning(request, "Cannot decrease quantity below 1.")
        else:
            messages.warning(request, f"Item '{product_name}' not found in cart.")

        return redirect('cart_dis')
    
def checkout(request): 
    if 'user' in request.session:
        data = signup.objects.get(username=request.session['user'])
        cart_items = Cart.objects.filter(user_data=data)

        if not cart_items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect('cart_dis')

        grouped_items = {}
        total = 0
        shipping = 0

        for item in cart_items:
            product_name = item.product_data.name
            quantity = item.quantity
            price = item.product_data.price
            product_image = item.product_data.image
            item_shipping = 299

            if product_name in grouped_items:
                grouped_items[product_name]['quantity'] += quantity
                grouped_items[product_name]['total'] += price * quantity
                grouped_items[product_name]['shipping'] += item_shipping * quantity
            else:
                grouped_items[product_name] = {
                    'quantity': quantity,
                    'price': price,
                    'total': price * quantity,
                    'image': product_image,
                    'shipping': item_shipping * quantity  # Comma added here
                }

        total_amount = sum(value['total'] for value in grouped_items.values())
        delivery_charge = sum(value['shipping'] for value in grouped_items.values())
        grand_total = total_amount + delivery_charge
        razorpay_total = grand_total * 100

        return render(request, 'checkout.html', {
            'cart_items': cart_items,
            'total_amount': total_amount,
            'grand_total': grand_total,
            'delivery_charge': delivery_charge,
            'razorpay_key': 'rzp_test_SROSnyInFv81S4',
            'razorpay_total': razorpay_total
        })

    return redirect('login')  # Redirect if user is not logged in


@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        payment_id = data.get('payment_id')
        user_id = data.get('user_id')  # Assuming user_id is part of the request
        billing_name = data.get('billing_name')
        billing_address = data.get('billing_address')
        shipping_name = data.get('shipping_name')
        shipping_address = data.get('shipping_address')
        total_amount = data.get('total_amount')

        user = signup.objects.get(pk=user_id)
        cart_items = Cart.objects.filter(user_data=user)

        # Create order and link cart items to it
        for cart_item in cart_items:
            Order.objects.create(
                user_data=user,
                product_data=cart_item.product_data,
                quantity=cart_item.quantity,
                billing_name=billing_name,
                billing_address=billing_address,
                shipping_name=shipping_name,
                shipping_address=shipping_address,
                total_amount=total_amount
            )
            
        # Clear cart after successful order
        Cart.objects.filter(user_data=user).delete()

        messages.success(request, "Payment successful. Your order has been placed.")
        return JsonResponse({'status': 'success'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def order_details(request):
    if 'user' in request.session:
        user = signup.objects.get(username=request.session['user'])
        orders = Order.objects.filter(user_data=user).order_by('-order_date')  # Fetch orders for the logged-in user
        return render(request, 'orders.html', {
            'orders': orders,
        })
    return redirect('login')  # Redirect to login if not logged in

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = signup.objects.get(useremail=email)
            token = default_token_generator.make_token(user)
            reset_link = f"{request.scheme}://{get_current_site(request).domain}/reset-password/{user.username}/{token}/"
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_link}',
                'admin@mywebsite.com',
                [email],
            )
            messages.success(request, "Password reset link sent to your email.")
        except signup.DoesNotExist:
            messages.error(request, "Email not found.")
    return render(request, "forgot-password.html")

def reset_password(request, username, token):
    try:
        user = signup.objects.get(username=username)
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password = request.POST.get('new_password')
                user.userpassword = new_password
                user.save()
                messages.success(request, "Password reset successfully.")
                return redirect('login')
            return render(request, 'reset-password.html', {'username': username, 'token': token})
        else:
            messages.error(request, "Invalid or expired token.")
            return redirect('login')
    except signup.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')

def productadminview(request, product_id):
    product = addproduct.objects.get(pk=product_id)
    
    # Get the current user's cart data for this product
    if 'user' in request.session:
        data = signup.objects.get(username=request.session['user'])
        cart_items = Cart.objects.filter(user_data=data)
        
        grouped_items = {}
        for item in cart_items:
            product_name = item.product_data.name
            quantity = item.quantity
            
            if product_name in grouped_items:
                grouped_items[product_name]['quantity'] += quantity
            else:
                grouped_items[product_name] = {
                    'quantity': quantity,
                    'product_data': item.product_data
                }
        
        # Check if the current product is in the cart
        product_in_cart = grouped_items.get(product.name, None)
    else:
        product_in_cart = None

    related_products = addproduct.objects.filter(category=product.category).exclude(pk=product.id)[:4]  # Limit to 4 products

    return render(request, 'productadminview.html', {
        'product': product,
        'related_products': related_products,  # Pass related products
        'product_in_cart': product_in_cart  # Pass the product info
    })
