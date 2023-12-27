from django.contrib import admin
from foodexpress_app.models import Profile, Category, Product, CartItem, Cart
# Register your models here.

admin.site.register([Profile, Category, Product, CartItem, Cart])
