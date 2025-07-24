from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User
class Location(models.Model):
city = models.CharField(max
_
length=50)
def
str
__
__
(self):
return self.city
class CarDealer(models.Model):
car
dealer = models.OneToOneField(User, on
delete=models.CASCADE)
_
_
phone = models.CharField(validators = [MinLengthValidator(10), MaxLengthValidator(10)], max
_
length =
