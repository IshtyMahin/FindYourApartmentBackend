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
        print(instance, serializer)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        print(serializer.validated_data)
        images_data = self.request.FILES.getlist('images')
        req_owner_id = serializer.validated_data['owner_id'] 
        apartment = serializer.save(owner_id=req_owner_id)
        print(images_data)
        print(req_owner_id)
        print(apartment)
        for image_data in images_data:
            ApartmentImage.objects.create(apartment=apartment, image=image_data)

    def perform_update(self, serializer):
        images_data = self.request.FILES.getlist('images')
        apartment = serializer.save()
        for image_data in images_data:
            ApartmentImage.objects.create(apartment=apartment, image=image_data)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = FavoriteApartment.objects.all()
    serializer_class = FavoriteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FavoriteApartmentFilter