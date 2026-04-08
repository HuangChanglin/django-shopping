from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, AddressViewSet

router = DefaultRouter()
router.register('addresses', AddressViewSet, basename='addresses')
router.register('', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]
