"""
URL configuration for foodexpress project.

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
from foodexpress_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),
    path('categories/<str:category_name>', views.categories, name='categories'),
    path('login/', views.log_in, name='login'),
    path('signup/', views.signup, name='signup'),
    path('product/<str:product_name>', views.product, name='product'),
    path('logout/', views.log_out, name='logout'),
    path('search/', views.search, name='search'),
    path('update_profile_address/', views.update_profile_address, name='update_profile_address'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('get_total_price/', views.get_total_price, name='get_total_price'),

]
