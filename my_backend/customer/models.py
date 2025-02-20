from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    star_count = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created = models.DateField(auto_now_add=True)
    
class WishItem(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True) 

class BasketItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='basketlist')
    count = models.IntegerField(default=0)
    size = models.ForeignKey('shop.Size', on_delete=models.CASCADE)
    color = models.ForeignKey('shop.Color', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
