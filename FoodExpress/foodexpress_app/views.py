from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

from foodexpress_app.forms import SettingsForm, LoginForm, RegisterForm
from foodexpress_app.models import Product, Category, Cart, CartItem, Profile


def index(request):
    if request.user.is_authenticated:
        user_carts = Cart.objects.filter(profile=request.user.profile)
        product_list = []
        for user_cart in user_carts:
            cart_items = user_cart.items.all()
            for cart_item in cart_items:
                product_list.append(cart_item)
        return render(request, 'index.html', {'cart': product_list})
    else:
        return render(request, 'index.html', {'cart': []})


@login_required(login_url='/login/', redirect_field_name='continue')
def settings(request):
    if request.method == 'GET':
        user_profile = Profile.manager.get(user=request.user.id)
        initial_data = {
            'username': request.user.username,
            'email': request.user.email,
            'address': user_profile.address,
        }
        settings_form = SettingsForm(initial=initial_data)
    elif request.method == 'POST':
        settings_form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if settings_form.is_valid():
            settings_form.save()
    else:
        settings_form = SettingsForm()
    return render(request, 'settings.html', {'settings_form': settings_form})


def categories(request, category_name):
    products = Category.manager.get_products_by_category(category_name)
    if request.user.is_authenticated:
        user_carts = Cart.objects.filter(profile=request.user.profile)
        product_list = []
        for user_cart in user_carts:
            cart_items = user_cart.items.all()
            for cart_item in cart_items:
                product_list.append(cart_item)
        return render(request, 'categories.html', {'products': products, 'category': category_name, 'cart': product_list})
    else:
        return render(request, 'categories.html',
                      {'products': products, 'category': category_name, 'cart': []})


def log_in(request):
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('continue', 'index'))
    return render(request, 'login.html', {'login_form': login_form})


def signup(request):
    if request.method == "GET":
        user_form = RegisterForm()
    if request.method == "POST":
        user_form = RegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            new_user = authenticate(request, username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'])
            if user:
                login(request, new_user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(None, "User saving error!")
    return render(request, 'signup.html', {'user_form': user_form})


def product(request, product_name):
    product = get_object_or_404(Product, name=product_name)
    products = Product.objects.all()

    if request.user.is_authenticated:
        user_carts = Cart.objects.filter(profile=request.user.profile)
        product_list = []

        for user_cart in user_carts:
            cart_items = user_cart.items.all()

            for cart_item in cart_items:
                product_list.append(cart_item)

        return render(request, 'product.html', {'product': product, 'cart': product_list, 'products': products})
    else:
        return render(request, 'product.html', {'product': product, 'products': products})


@login_required(login_url='/login/', redirect_field_name='continue')
def log_out(request):
    auth.logout(request)
    return redirect(reverse('login'))


@login_required(login_url='/login/', redirect_field_name='continue')
def update_profile_address(request):
    if request.method == 'POST':
        address = request.POST.get('address', '')
        profile = request.user.profile  # Предполагается, что у пользователя есть профиль
        profile.address = address
        profile.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required(login_url='/login/', redirect_field_name='continue')
def get_total_price(request):
    user_cart = Cart.objects.filter(profile=request.user.profile).first()

    if user_cart:
        total_price = sum(item.product.price * item.quantity for item in user_cart.items.all())
        return JsonResponse({'total_price': total_price})
    else:
        return JsonResponse({'total_price': 0})


@login_required(login_url='/login/', redirect_field_name='continue')
def update_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')

        try:
            product = Product.objects.get(id=product_id)

            user_carts = Cart.objects.filter(profile=request.user.profile)

            if user_carts.exists():
                user_cart = user_carts.first()
            else:
                user_cart = Cart.objects.create(profile=request.user.profile)

            cart_item = None

            for current_cart_item in user_cart.items.all():
                if current_cart_item.product == product:
                    if action == 'increment':
                        current_cart_item.quantity += 1
                        current_cart_item.save()
                        cart_item = current_cart_item
                    elif action == 'decrement':
                        if current_cart_item.quantity >= 1:
                            current_cart_item.quantity -= 1
                            if current_cart_item.quantity == 0:
                                user_cart.items.remove(current_cart_item)
                                current_cart_item.delete()
                            current_cart_item.save()
                            cart_item = current_cart_item

            if not cart_item and action == 'increment':
                cart_item = CartItem.objects.create(cart=user_cart, product=product, quantity=1)
                user_cart.items.add(cart_item)

            if cart_item:
                return JsonResponse({'success': True, 'quantity': cart_item.quantity})
            else:
                return JsonResponse({'success': False, 'error': 'Cart item not found for the specified product'})

        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

