from django_filters import rest_framework as filters
from .models import Apartment
from .models import FavoriteApartment
class ApartmentFilter(filters.FilterSet):
    division = filters.CharFilter(field_name='division', lookup_expr='icontains')
    partial_address = filters.CharFilter(field_name='address', lookup_expr='icontains')
    size = filters.NumberFilter(field_name='size',lookup_expr='gte')
    bed = filters.NumberFilter(field_name='bed',lookup_expr='gte')
    bath = filters.NumberFilter(field_name='bath',lookup_expr='gte')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Apartment
        fields = ['division', 'partial_address', 'size', 'bed', 'bath', 'min_price', 'max_price']
        
        
class FavoriteApartmentFilter(filters.FilterSet):
    user = filters.CharFilter(field_name='user')
    apartment = filters.CharFilter(field_name='apartment')
    


