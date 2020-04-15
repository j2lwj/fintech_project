from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    p_name = models.CharField(max_length=50, unique=True)
    p_desc = models.CharField(max_length=200)
    cum_return = models.FloatField()
    cagr = models.FloatField()
    sharpe = models.FloatField()
    max_drawdown = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='portfolio', on_delete=models.CASCADE)

    class Meta:
        db_table = 'portfolio'

    def __str__(self):
        return self.p_name, self.p_desc

class User_Portfolio(models.Model):
    user_id = models.ForeignKey(User, related_name='user_portfolio', on_delete=models.CASCADE, db_column = 'user_id')
    portfolio_id = models.ForeignKey(Portfolio, related_name='user_portfolio', on_delete=models.CASCADE, db_column = 'portfolio_id')

    class Meta:
        db_table = 'user_portfolio'

    def __str__(self):
        return self.user_id, self.portfolio_id 

class Stocks(models.Model):
    stock_id = models.AutoField(primary_key=True)
    stock_name = models.CharField(max_length=20, unique=True)
    ticker = models.CharField(max_length=10, unique=True)
    forecast_return = models.FloatField(default=0)
    mse = models.FloatField(default=0)

    class Meta:
        db_table = 'stocks'
    
    def __str__(self):
        return self.stock_name
    

class Portfolio_Stocks(models.Model):
    port_id = models.ForeignKey(Portfolio, related_name='portfolio_stocks', on_delete=models.CASCADE, db_column = 'port_id')
    stock_id = models.ForeignKey(Stocks, related_name='portfolio_stocks', on_delete=models.CASCADE, db_column = 'stock_id')
    stock_weight = models.FloatField()
    
    class Meta:
        db_table = 'portfolio_stock'
    
    def __str__(self):
        return self.port_id, self.stock_id