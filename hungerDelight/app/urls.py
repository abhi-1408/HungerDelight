
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index),
    path('merchant/', views.all_merchant_view),
    path('store/', views.all_store_view),
    path('item/', views.all_item_view),
]
