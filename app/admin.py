from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(signup)
admin.site.register(signinn)

admin.site.register(addproduct)
admin.site.register(updateproduct)

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Wishlist)
