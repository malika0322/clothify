from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home/', views.index, name="home"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("contact/", views.contact, name="contact"),
    path("shop/<str:option_name>", views.shop, name="shop"),
    path('overview/<int:id>',views.product_overview,name='product_overview'),
    path('policy/', views.policy, name='policy'),
    path('faqs/', views.faqs, name='faqs'),
    
    path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('order_page/', views.order_page, name='order_page'),
    path('login/',views.login_page,name='login_page'),
    path('logout/',views.logout_page,name='logout_page'),
    path('register/', views.register_page, name='register_page'),
    path('remove_from_cart/<int:id>', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/<int:id>',views.checkout,name='checkout'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

]

