from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from django.contrib.auth import authenticate,login
from django.contrib import messages
from .forms import modelform
# Create your views here.

def register(request):

    if request.method== "POST":
        a=request.POST["username"]
        b=request.POST["your_email"]
        c=request.POST["password"]
        try:
            k=signup.objects.get(username=a)
            print(k.username)
            if k is not None:
                messages.error(request,'already exits')
        except:
            myuser=signup.objects.create(username=a,your_email=b,password=c)
            myuser.save()
    return render(request,"signup.html")

def signin(request):

    if request.method== "POST":
        x=request.POST["myname"]
        y=request.POST["mypass"]
        try:
            data=signup.objects.get(username=x)
            if y==data.password:
                request.session['user']=x
                return render(request,"profile.html")
            else:
                return render(request,"index.html")
        except Exception:
            if x=="admin" and y=="admin":
                request.session['admin']=x
                return render(request,"admin.html")
            else:
                messages.error(request,"Error Invalid Admin")

    return render(request,"login.html")
# written by neethu  
# def profile(re):
#     if 'user' in re.session:
#         h=signup.objects.get(username=re.session['user'])
#         data=addproduct.objects.all()
#         l=[]
#         data1=cartitems.objects.filter(user_data=h)
#         for i in data1:
#             print(i)
#             l.append(i.product_data)
#         print(l)

#         return render(re,'profile.html',{'h':h.username,'dd':data,'l':l})
    
#     return render(re,'profile.html')

# def profile(request):
#     if request.user.is_authenticated:
#         data = addproduct.objects.all()
#         cart_items = cartitems.objects.filter(user=request.user)
#         return render(request, 'profile.html', {'user': request.user, 'products': data, 'cart_items': cart_items})
#     return redirect('login')

def home(re):
    data=addproduct.objects.all()
    
    return render(re,'index.html',{"d":data})

def shoppage(re):
    shop_data=addproduct.objects.all()
    return render(re,'shop.html',{"d":shop_data})

def sub(re):
    return render(re,'home.html')

def adminpage(request):
    return render(request,"admin.html")

def addproductpage(request):
    if 'admin' in request.session:
        if request.method== "POST": 
            a=request.POST["productname"]
            b=request.POST["productcat"]
            c=request.POST["productdes"]
            d=request.POST["price"]
            e=request.FILES["productimg"]
            f=request.POST["productinfo"]
            g=request.POST["productsize"]
            h=request.POST["productcolor"]
            i=request.POST["discountprice"]
            myprod=addproduct.objects.create(productname=a,productcat=b,productdes=c,price=d,productimg=e,productinfo=f,productsize=g,productcolor=h,discountprice=i)
            myprod.save()

        return render(request,"addproducts.html")

def viewproductpage(request):
    data=addproduct.objects.all()
    return render(request,"viewproducts.html",{"d":data})
def shopdetailpage(re,p):
    shop_details=addproduct.objects.get(pk=p)
    return render(re,'shopdetails.html',{"p":shop_details})


def supportpage(request):
    return render(request,"support.html")
def selectaddproduct(request):
    return render(request,"addproductselector.html")
def product_detail(request):
  

    return render(request,"detail.html")

def profilepage(request):
    if 'user' in request.session:
        h=signup.objects.get(username=request.session['user'])
        data=addproduct.objects.all()
        l=[]
        data1=cartitems.objects.filter(user_data=h)
        for i in data1:
            print(i)
            l.append(i.product_data)
        print(l)
        return render(request,"profile.html",{'h':h.username,'dd':data,'l':l})

    return redirect(request,"login.html")

def userform(request):
    if request.method== 'POST':
        s=modelform(request.POST)
        if s.is_valid():
            s.save()
            return HttpResponse("Form Save Successfully")
    s=modelform()
    return render(request,'userregister.html',{'r':s})

def updateproductpage(request,d):
    if request.method== "POST":
        a1=request.POST["productname"]
        b1=request.POST["productcat"]
        c1=request.POST["productdes"]
        d1=request.POST["price"]
        e1=request.FILES["productimg"]
        
        addproduct.objects.filter(productname=a1).update(productcat=b1,productdes=c1,price=d1,productimg=e1)
        messages.success(request,'Product Updated Sucessfully')
        return redirect(viewproductpage)
    data=addproduct.objects.get(pk=d)
    return render(request,"updateproductpage.html",{"d":data})

def dele(re,s):
    l=addproduct.objects.get(pk=s)
    l.delete()
    messages.success(re,"Deleted")
    return redirect(viewproductpage)
# found online
# def view_cart(request):
    
#     cart_item = cartitems.objects.filter(user=request.user)
#     total_price = sum(item.product.price * item.quantity for item in cart_items)
#     return render(request, 'cart.html', {'cart_items': cart_item, 'total_price': total_price})

# def add_to_cart(request, product_id):
#     if 'user' in request.session:

#         product = addproduct.objects.get(id=product_id)
#         try:
#             cart=cartitems.objects.get(cart_id=_cartitems_id(request))
#         except cart.DoesNotExist:
#             cart=cartitems.objects.create(cart_id=_cartitems_id(request))
#             cart.save()

#         try:
#             cart_item=CartItem.objects.get(product=product,cart=cart)
#             cart_item.quantity += 1
#             cart_item.save()
#         except CartItem.DoesNotExist:
#             cart_item=CartItem.objects.create(
#                 product=product,
#                 quantity=1,
#                 cart=cart,
#             )
#             cart_item.save()
#             data=CartItem.objects.get(pk=product_id)
#     return render('cart',{"product_id":data})

def logout(re):
    if 'user' in re.session or 'admin' in re.session:
        re.session.flush()
        return redirect(signin)
    
# written by neethu
# def cartsummary(request,s):
#     if 'user' in request.session:
#         data=signup.objects.get(username=request.session['user'])
#         l=addproduct.objects.get(pk=s)

#         user_cart=cartitems.objects.create(user_data=data,product_data=l)
#         user_cart.save()
#         messages.success(request,"Saved to cart successfully")

#     return redirect(request,"profile.html")



# def cartdisplay(re):
#     if 'user' in re.session:
#         data=signup.objects.get(username=re.session['user'])
#         d=cartitems.objects.filter(user_data=data)
#         return render(re,"usercart.html",{'dd':d})


# def removecart(re,cart_items_id):
#     if 'user' in re.session:
#         cartitems.objects.filter(pk=cart_items_id)
#         cartitems.delete()
#         messages.success(re,"Removed From Cart Successfully")
#         return redirect(re,'cartdisplay')


# def cartsummary(request, product_id):
#     if request.user.is_authenticated:
#         product = get_object_or_404(addproduct, pk=product_id)
#         cart_item, created = cartitems.objects.get_or_create(user=request.user, product=product)
#         if not created:
#             cart_item.quantity += 1
#             cart_item.save()
#         messages.success(request, "Added to cart successfully")
#     return redirect('profile')

# def cartdisplay(request):
#     if request.user.is_authenticated:
#         cart_items = cartitems.objects.filter(user=request.user)
#         return render(request, "usercart.html", {'cart_items': cart_items})
#     return redirect('login')

# def removecart(request, cart_item_id):
#     if request.user.is_authenticated:
#         cart_item = get_object_or_404(cartitems, pk=cart_item_id, user=request.user)
#         cart_item.delete()
#         messages.success(request, "Removed from cart successfully")
#     return redirect('cartdisplay')

def user_profile(re):
    if 'user' in re.session:
        h=signup.objects.get(username=re.session['user'])
        data = addproduct.objects.all()
        l=[]
        data1=cartitems.objects.filter(user_data=h)
        for i in data1:
            print(i)
            l.append(i.product_data)
        print(l)

        return render(re,'userprofile.html',{'h':h.username,'dd':data,'l':l})

    return redirect(signin)

def cart(re,s):
    if 'user' in re.session:
        data=signup.objects.get(username=re.session['user'])
        l=addproduct.objects.get(pk=s)

        user_cart=cartitems.objects.create(user_data=data,product_data=l)
        user_cart.save()
        messages.success(re,"successfully")


    return redirect(user_profile)

def cart_dis(re):
    if 'user' in re.session:
        data=signup.objects.get(username=re.session['user'])
        d=cartitems.objects.filter(user_data=data)
        qty=0
        total=0
        for i in d:
            qty += i.quantity
            total += i.product_data.price * i.quantity
        
        if not d:
            messages.info(re, 'No items in the cart.')
            return render(re,'viewproducts.html')

        return render(re,'cart.html',{'dd':d,'total': total, 'qty': qty})
    return redirect('')

def cart_remove(re,t):
    if 'user' in re.session:
        cartitems.objects.filter(pk=t).delete()
        messages.success(re,"remove successfully")
        return redirect(cart_dis)
def productdetailpage(request,d):
    product =addproduct.objects.get(pk=d)
    return render(request,'detail.html',{'d': product})