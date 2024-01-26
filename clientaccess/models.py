from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import int_list_validator

# Create your models here.
class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()
    details = models.CharField(max_length=200)

    def __str__(self):
        return self.id
    
class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.IntegerField()
    items = models.CharField(validators=[int_list_validator], max_length=100, null =True) 
    order_date = models.DateField(default=datetime.date.today)
    default_deliver_date = datetime.date.today() + datetime.timedelta(days=10)
    deliver_date = models.DateField(default=default_deliver_date)

    def __str__(self):
        return self.id
    
class ShoppingCart(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.IntegerField()
    item = models.IntegerField(null = True)

    def __str__(self):
        return self.id