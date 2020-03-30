from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    p_name = models.CharField(max_length=50, unique=True)
    p_desc = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='portfolio', on_delete=models.CASCADE) 

    def __str__(self):
        return self.p_name, self.p_desc

class User_Portfolio(models.Model):
    user_id = models.ForeignKey(User, related_name='user_portfolio', on_delete=models.CASCADE)
    portfolio_id = models.ForeignKey(Portfolio, related_name='user_portfolio', on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id, self.portfolio_id 

class Stocks(models.Model):
    stock_id = models.AutoField(primary_key=True)
    stock_name = models.CharField(max_length=20, unique=True)
    ticker = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.stock_name

class Portfolio_Stocks(models.Model):
    port_id = models.ForeignKey(Portfolio, related_name='portfolio_stocks', on_delete=models.CASCADE)
    stock_id = models.ForeignKey(Stocks, related_name='portfolio_stocks', on_delete=models.CASCADE)

    def __str__(self):
        return self.port_id, self.stock_id