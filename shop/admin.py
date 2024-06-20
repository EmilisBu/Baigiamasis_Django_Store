from django.contrib import admin
from .models import UserProfile, Item, Cart, CartItem

admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'is_discount', 'discount_price')
    list_filter = ('is_discount',)
    fields = ['name', 'description', 'price', 'quantity', 'is_discount', 'discount_price', 'image']
