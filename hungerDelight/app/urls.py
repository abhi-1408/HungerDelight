from django.urls import path, include
from .views import MerchantViewSet, ItemViewSet, StoreViewSet, OrderViewSet, webhook_acknowledge
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('merchant', MerchantViewSet)
router.register('store', StoreViewSet)
router.register('item', ItemViewSet)
router.register('order', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('webhook/', webhook_acknowledge, name="webhook")
]
