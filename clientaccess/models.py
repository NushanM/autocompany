from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()
    details = models.CharField(max_length=200)

    def __str__(self):
        return self.id
    
class Order(models.Model):
    order_id = models.IntegerField()
    user_id = models.IntegerField()
    item_id = models.IntegerField(null = True)
    quantity = models.IntegerField(default = 1)
    order_date = models.DateField(default=datetime.date.today)
    default_deliver_date = datetime.date.today() + datetime.timedelta(days=10)
    deliver_date = models.DateField(default=default_deliver_date)

    def __str__(self):
        return self.order_id
    
class ShoppingCart(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    item_id = models.IntegerField(null = True)
    quantity = models.IntegerField(default = 1)


    def __str__(self):
        return self.id