from django.contrib import admin
from .models import Portfolio, User_Portfolio, Stocks, Portfolio_Stocks
# Register your models here.
admin.site.register(Portfolio)
admin.site.register(User_Portfolio)
admin.site.register(Stocks)
admin.site.register(Portfolio_Stocks)