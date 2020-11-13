from django.shortcuts import render
from .models import Item

def HomeView(request):
    return render(request, 'home-page.html')

def ProductView(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'product-page.html', context)

def CheckoutView(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'checkout-page.html', context)