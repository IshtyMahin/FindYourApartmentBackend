from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Apartment,ApartmentImage,FavoriteApartment,Booking

from .serializers import ApartmentSerializer,FavoriteSerializer,BookingSerializer

from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ApartmentFilter,FavoriteApartmentFilter

    
class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApartmentFilter
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        apartment = serializer.save()
        image_urls = self.request.data.get('uploaded_images', [])
        for url in image_urls:
            ApartmentImage.objects.create(apartment=apartment, image_url=url)

    def perform_update(self, serializer):
        apartment = serializer.save()
        image_urls = self.request.data.get('uploaded_images', [])
        for url in image_urls:
            ApartmentImage.objects.create(apartment=apartment, image_url=url)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = FavoriteApartment.objects.all()
    serializer_class = FavoriteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FavoriteApartmentFilter