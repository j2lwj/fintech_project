from django.db import models
from django.contrib.auth.models import User
# from django.contrib.postgres.fields import ArrayField

# Class: Portfolio, Stocks, (User)
class Portfolio(models.Model):
    created_by = models.ForeignKey(User, related_name='portfolio', on_delete=models.CASCADE)
    p_name = models.CharField(max_length=50, unique=True)
    saved_at = models.DateTimeField(auto_now_add=True)
    # stocks details (e.g. ticker, price) will be extracted from another static database, hence no class
    # allocation = ArrayField()


# class Stocks(models.Model):
#     s_name = models.CharField(max_length=50)
#     price = models.FloatField()

# class Port_stocks(models.Model):
#     portfolio = models.ForeignKey(Portfolio, related_name="port_stocks")
    