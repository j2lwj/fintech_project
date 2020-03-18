from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, QueryDict, HttpResponseRedirect, Http404, JsonResponse
import requests
import pandas as pd
from datetime import datetime
# from stocks import app, db
# from stocks.models import StockPrice
# from .models import StockPrice
# from flask import request, jsonify, render_template, Response
from bs4 import BeautifulSoup
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.layouts import widgetbox
from bokeh.embed import components

# Create your views here.
def login(request):
    return render(request, "<p>Helllo</p>")

def home(request):
    return render(request, "index.html")

def my_portfolio(request):
    return render(request, "<p>Helllo</p>")

def compare(request):
    return render(request, "<p>Helllo</p>")


def portfolios(request):
    return render(request, 'index.html')
