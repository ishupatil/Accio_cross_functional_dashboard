from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('showrooms/', views.showrooms, name='showrooms'),
    path('customers/', views.customers, name='customers'),
    path('regions/', views.regions, name='regions'),
    path('simulator/', views.simulator, name='simulator'),
    path('inventory/', views.inventory, name='inventory'),
]
