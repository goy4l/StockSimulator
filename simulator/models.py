from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class league(models.Model):
    users = models.ManyToManyField(User, related_name="league")
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    game_code = models.CharField(max_length=1000)
    starting_balance = models.IntegerField()

