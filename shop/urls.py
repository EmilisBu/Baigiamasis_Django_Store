from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='item_list'), name='logout'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('new_additions/', views.new_additions, name='new_additions'),
    path('discounts/', views.discounts, name='discounts'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('about_us/', views.about_us, name='about_us'),
    path('my_orders/', views.my_orders, name='my_orders'),
]
