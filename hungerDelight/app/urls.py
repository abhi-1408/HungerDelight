
from django.contrib import admin
from django.urls import path, include
from .views import MerchantViewSet, ItemViewSet, StoreViewSet, OrderViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('merchant', MerchantViewSet)
router.register('store', StoreViewSet)
router.register('item', ItemViewSet)
router.register('order', OrderViewSet)

urlpatterns = [

    path('', include(router.urls)),


]
