from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView
from .models import Item, OrderItem, Order
from django.contrib.messages import constants as messages


class HomeView(ListView):
    model = Item
    template_name = 'home.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"



def CheckoutView(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'checkout.html', context)



def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user = request.user,
        ordered = False
        )
    order_qs = Order.objects.filter(user=request.user , ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "This item was already added to your cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, "This item was added to your cart")

    return redirect("core:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user = request.user,
        ordered = False
    )

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item, created = OrderItem.objects.get_or_create(
                item=item,
                user = request.user,
                ordered = False
            )[0]
            order.items.remove(order_item)
    else:
        # add a message saying the user doesnt have an order
        return redirect("core:product", slug=slug)
        
    return redirect("core:product", slug=slug)