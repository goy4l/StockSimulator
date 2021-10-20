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
    def __str__(self):
        return f"{self.name}"

class lauth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    league = models.ForeignKey(league,on_delete=models.CASCADE)
    balance = models.IntegerField()

class stocks(models.Model):
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    price = models.IntegerField()
    league = models.ForeignKey(league, on_delete=models.CASCADE, related_name="stocks")
    
    class Meta:
        verbose_name_plural = "Stocks"

class news(models.Model):
    title = models.CharField(max_length=10000)
    stock = models.ForeignKey(stocks, on_delete=models.CASCADE, related_name="news")
    description = models.CharField(max_length=100000)
    created_at = models.DateTimeField(auto_now_add=True)
    league = models.ForeignKey(league, on_delete=models.CASCADE, related_name="news")

    class Meta:
        verbose_name_plural = "News"

class holdings(models.Model):
    stock = models.ForeignKey(stocks, on_delete=models.CASCADE, related_name='holdings')
    quantity = models.IntegerField()
    average_price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='holdings')
    created_at = models.DateTimeField(auto_now_add=True)
    league = models.ForeignKey(league, on_delete=models.CASCADE, related_name="holdings")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Holdings"
    
class transaction(models.Model):
    ttype_choices = (('BUY','BUY'),('SELL','SELL'))
    ttype = models.CharField(max_length=100,choices = ttype_choices)
    stock = models.ForeignKey(stocks, on_delete=models.CASCADE, related_name='transaction')
    quantity = models.IntegerField()
    buy_price = models.IntegerField()
    total_investment = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='transaction')
    created_at = models.DateTimeField(auto_now_add=True)
    league = models.ForeignKey(league, on_delete=models.CASCADE, related_name="transaction")


class transfer(models.Model):
    ttype_choices = (('PENDING','PENDING'),('ACCEPTED','ACCEPTED'),('DECLINED','DECLINED'),('INVALID','INVALID'))
    stock = models.ForeignKey(stocks, on_delete=models.CASCADE, related_name='transfer')
    quantity = models.IntegerField()
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='transfer_to')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='transfer_from')
    league = models.ForeignKey(league, on_delete=models.CASCADE, related_name="transfer")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,choices = ttype_choices)
    active = models.BooleanField()