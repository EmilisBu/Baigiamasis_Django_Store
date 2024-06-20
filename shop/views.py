from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm
from .models import Item, Cart, CartItem, CompletedCart, CompletedCartItem
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta


def item_list(request):
    items = Item.objects.all()
    return render(request, 'shop/item_list.html', {'items': items})


def discounts(request):
    items = Item.objects.filter(is_discount=True)
    return render(request, 'shop/discounts.html', {'items': items})


def new_additions(request):
    one_week_ago = timezone.now() - timedelta(days=7)
    items = Item.objects.filter(date_added__gte=one_week_ago)
    return render(request, 'shop/new_additions.html', {'items': items})


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'shop/view_cart.html', {'cart_items': cart_items})


def register(request):
    if request.user.is_authenticated:
        return redirect('item_list')
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('item_list')
        else:
            print("User form errors:", user_form.errors)
            print("Profile form errors:", profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'shop/register.html', {'user_form': user_form, 'profile_form': profile_form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('item_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('item_list')


def contact_us(request):
    return render(request, 'shop/contact_us.html')


def about_us(request):
    return render(request, 'shop/about_us.html')


@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Make sure there is only 1 cart active
    if not created:
        Cart.objects.filter(user=request.user).exclude(id=cart.id).delete()

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        if cart_item.quantity < item.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.error(request, 'Cannot add more of this item, not enough stock.')
    else:
        cart_item.save()

    # stay on same page you are now on if clicked add to cart
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('item_list')


@login_required
def my_orders(request):
    orders = CompletedCart.objects.filter(user=request.user).prefetch_related('completedcartitem_set')
    orders = [order for order in orders if order.completedcartitem_set.exists()]
    return render(request, 'shop/my_orders.html', {'orders': orders})


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        completed_cart = CompletedCart.objects.create(user=request.user)
        for cart_item in cart.cartitem_set.all():
            item = cart_item.item
            if cart_item.quantity > item.quantity:
                messages.error(request, f'Not enough stock for {item.name}.')
                return redirect('view_cart')
            CompletedCartItem.objects.create(
                cart=completed_cart,
                item=item,
                quantity=cart_item.quantity
            )
            item.quantity -= cart_item.quantity
            item.save()
        cart.cartitem_set.all().delete()
        cart.delete()  # Clear cart after
        messages.success(request, 'Checkout completed successfully.')
        return redirect('item_list')
    return render(request, 'shop/checkout.html', {'cart': cart})


@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, item_id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')
