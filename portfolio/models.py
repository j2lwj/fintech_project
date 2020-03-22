from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

#https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/fields/ --> Documentation for ArrayField
# Class: Portfolio, Stocks, (User)
class Portfolio(models.Model):
    p_name = models.CharField(max_length=50, unique=True)
    p_desc = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='portfolio', on_delete=models.CASCADE)
    stocks = ArrayField(models.CharField(max_length=5), default=list)

    def __str__(self):
        return self.p_name
    # stocks details (e.g. ticker, price) will be extracted from another static database, hence no class


# class Stocks(models.Model):
#     s_name = models.CharField(max_length=50)
#     price = models.FloatField()

# class Port_stocks(models.Model):
#     portfolio = models.ForeignKey(Portfolio, related_name="port_stocks")
    