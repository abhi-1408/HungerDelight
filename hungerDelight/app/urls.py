
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index),
    path('merchant/', views.merchant_list_view),
    path('merchant/<int:pk>/', views.merchant_detail_view),
    path('store/', views.store_list_view),
    path('store/<int:pk>/', views.store_detail_view),
    path('item/', views.item_list_view),
    path('item/<int:pk>/', views.item_detail_view),
]
