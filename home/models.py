from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name 
   

class Product(models.Model):
    

    product_name=models.CharField(max_length=100)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    product_image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) 
    stock = models.PositiveIntegerField(default=1)
    likes = models.IntegerField(default=0)
    wishlist_users = models.ManyToManyField(User, related_name="wishlist", blank=True)
    # size = models.CharField(max_length=10, default='M')
    def __str__(self):
        return self.product_name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.product_name} - {self.quantity}'
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class OrderedBy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    process = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} time:{self.date}"

class Ordered(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=100)
    orderedby = models.ForeignKey(OrderedBy, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.product_name}"
    
class wishlist(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Add any other fields you need for the wishlist

    def __str__(self):
        return f"Wishlist of {self.product.name}"