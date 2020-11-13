from django.urls import path
from .views import HomeView, ProductView, CheckoutView

app_name = 'core'

urlpatterns = [
    path('', HomeView, name='home'),
    path('products/', ProductView, name='products'),
    path('checkout/', CheckoutView, name='checkout'),
]