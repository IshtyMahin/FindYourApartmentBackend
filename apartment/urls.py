from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ApartmentViewSet,BookingViewSet,FavoriteViewSet

router = DefaultRouter()
router.register(r'list', ApartmentViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'favorites', FavoriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
