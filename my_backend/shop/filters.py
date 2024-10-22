import django_filters as filters
from .models import Product

class ProductFilter(filters.Filter):
    min_price=filters.NumberFilter(field_name='price',lookup_expr='gte')
    max_price=filters.NumberFilter(field_name='price',lookup_expr='lte')

class Meta:
    model=Product
    fields= ['sizes','colors','categories']
