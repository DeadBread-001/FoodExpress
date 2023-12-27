from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class ProfileManager(models.Manager):
    def get_user_by_id(self, user_id):
        return User.objects.get(pk=user_id)

    def get_profile_by_id(self, user_id):
        return Profile.manager.get(user_id=user_id)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    manager = ProfileManager()

    def __str__(self):
        return self.user.username


class CategoryManager(models.Manager):
    def get_products_by_category(self, category):
        category = Category.manager.get(name=category)
        return category.products.all()


class Category(models.Model):
    name = models.CharField(max_length=100)
    manager = CategoryManager()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    weight = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.CharField(max_length=255, default='default.png')

    def __str__(self):
        return self.name


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cart')
    items = models.ManyToManyField('CartItem')
