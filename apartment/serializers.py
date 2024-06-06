from rest_framework import serializers
from .models import Apartment, ApartmentImage,FavoriteApartment,Booking

class ApartmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentImage
        fields = ['id', 'image_url', 'apartment']

class ApartmentSerializer(serializers.ModelSerializer):
    images = ApartmentImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.URLField(), write_only=True
    )

    class Meta:
        model = Apartment
        fields = ['id', 'price', 'address', 'bed', 'bath', 'division', 'size', 'description', 'last_update', 'owner_id', 'images', 'uploaded_images']
        
    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        apartment = Apartment.objects.create(**validated_data)
        for url in uploaded_images:
            ApartmentImage.objects.create(apartment=apartment, image_url=url)
        return apartment
        

    
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'apartment', 'bookingDateTime', 'createdAt']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteApartment
        fields = ['id', 'user', 'apartment', 'createdAt']