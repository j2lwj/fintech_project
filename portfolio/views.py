# Django Library
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, QueryDict, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Python Library
import requests
import datetime
import json
import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter
from math import pi
from bs4 import BeautifulSoup

# Bokeh Libraries
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool, Legend
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.layouts import widgetbox
from bokeh.embed import components
from bokeh.palettes import Category20c, Spectral11
from bokeh.transform import cumsum

# Local Libraries
from .models import Portfolio, User_Portfolio, Stocks, Portfolio_Stocks
from .forms import SignUpForm

# after finalizing the models.py --> from .models import Stocks, Port_stocks

# Create your views here.
"""
To-do-list:
1. Find a way for django to access stocks db
2. Create a bokeh for every portfolio created 
3. 
"""
def log_in(request):
    #receive input from form - method=GET from user database, inputs: email, password
    #login function - input submit button, access my_portfolio html
    #sign-up button - href to sign-up html
    username = request.POST.get['username']
    password = request.POST.get['password']
    user = authenticate(request, username=username, password=password) 
    if user is not None:
        login(request, user)
        return redirect('my_portfolio')
    else:
        return render(request, "login.html")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('my_portfolio') 
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form}) 

def log_out(request):
    logout(request)
    return redirect('home')

def home(request):
    #only have log-in button - href to login html 
    return render(request, "main_home.html")

def main_forecast(request):

    import pandas as pd
    df = pd.read_excel('sector_MSE.xlsx', index_col=0)  
    columns = df.columns.tolist()

    numlines=len(df.columns)
    mypalette=Spectral11[0:numlines]

    data = {
        'xs': [df.index.values]*numlines,
        'ys': [df[name].values for name in df],
        'labels': columns,
        'color': mypalette
        }

    source = ColumnDataSource(data)

    p = figure(width=1000, height=300, x_axis_type="datetime", title='MSE per Industry') 
    p.multi_line(xs='xs', ys='ys', legend='labels', source=source, line_color='color', line_width=3)
       
    p.background_fill_color = None
    p.border_fill_color = None
    p.xgrid.grid_line_color = None

    p.title.text_font = "gill"
    p.title.text_font_size = "20px"
    p.xaxis.major_label_text_font = "gill"
    p.xaxis.major_label_text_font_size = "18px"
    p.yaxis[0].formatter = NumeralTickFormatter(format="0.00%")
    p.yaxis.major_label_text_font = "gill"
    p.yaxis.major_label_text_font_size = "18px"

    new_legend = p.legend[0]
    p.legend[0].plot = None
    p.add_layout(new_legend, 'right')

    p.legend.label_text_font = "gill"
    p.legend.label_text_font_size = "12px"

    p.add_tools(HoverTool(tooltips=[("Sector", "@labels"), ("MSE", "$y{1.11%}")]))

    script, div = components(p)

    context = {
        'script': script,
        'div': div
    }

    return render(request, "main_forecast.html", context=context)

def main_optimize(request):
    return render(request, "main_optimize.html")

def my_portfolio(request):
    # GRAPHS
        
    # Work-In-Progress: linking the 'Forecast' button to the variables in 'p'

    # stocks = request.POST.get("array of stocks")
    stocks = ['AAPL', 'UNM', 'VIAV']

    context = {
        'stocks': stocks
    }
  
    if stocks is None:
        return render(request=request, template_name='homepage.html', context=context)
    
    try:

        stocks_db = Stocks.objects.all()
        
        # Dummy data
        df = {'stock_name':['AAPL','GOOGL'],'forecast_return': [1,2]} 
        
        #df = pd.read_csv('')  #Code to append to selected_portfolios --> {'stock_name': [], 'predicted_returns': []}

    except KeyError:
        script = None
        div = None
    else:
        p = figure(x_range = df['stock_name'], plot_height=300, plot_width=1000, title="Predicted Returns",
                toolbar_location=None, tools="")
        p.vbar(x = df['stock_name'], top = df['forecast_return'], width = 0.9, hover_color="pink")
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        p.background_fill_color = None
        p.border_fill_color = None
        p.title.text_font = "gill"
        p.title.text_font_size = "24px"
        p.title.text_color = "white"
        p.yaxis.axis_label = "Predicted Returns"
        p.yaxis.axis_label_text_font = "gill"
        p.yaxis.axis_label_text_font_size = "16px"
        p.yaxis.axis_label_text_color = "white"
<<<<<<< HEAD
=======
        p.yaxis[0].formatter = NumeralTickFormatter(format="0.000%")
>>>>>>> 35b52fa5d4754ec5f6167bbd16639f0fa0ec9ad4
        p.xaxis.major_label_text_font = "gill"
        p.xaxis.major_label_text_font_size = "20px"
        p.xaxis.major_label_text_font_style = "bold"
        p.xaxis.major_label_text_color = "white"
        p.yaxis.major_label_text_font = "gill"
        p.yaxis.major_label_text_font_size = "20px"
        p.yaxis.major_label_text_color = "white"
        p.add_tools(HoverTool(tooltips=[("Stock", "@stock_name"), ("Predicted Returns", "@predicted_returns")]))
        
        script, div = components(p)

    ''' Create Stocks Objects: Already done, do not uncomment to avoid duplicating stocks objects '''

    # stocks_df = pd.read_csv('tickers_latest.csv')
    # tup = stocks_df.values

    # for each in tup:
    #     Stocks.objects.create(stock_id=each[0], stock_name=each[2], ticker=each[1], forecast_return=each[3], mse=each[4])
   
    ''' Link front end stocks selection inputs to back-end '''
    
    # idArr contains a list of user-selected stock tickers
    selected_stocks = request.POST.get("idArray")

    # Retrieve Stock model object's ticker based on selected stocks, append the tickers into a dictionary (stock_dict) to return to user for future use
    stock_dict = {}
<<<<<<< HEAD

    if selected_stocks is not None: 

=======

    if selected_stocks is not None: 

>>>>>>> 35b52fa5d4754ec5f6167bbd16639f0fa0ec9ad4
        for each in selected_stocks:
            count = 1
            # Assigns every user selected stock to a dictionary key. E.g. stock_dict = {'stock_1':{'ticker':'AAPL', 'forecasted_return': 0.01234}}
            stock_dict["stock_{}".format(count)] = {'ticker': each, 'forecasted_return': Stocks.objects.get(ticker=each).forecast_return}
            count += 1

    ''' ML Model: inputs- idArray'''
    # Insert ML Model here

    # store output to mlOutput to be passed to front end, which will then jump to optimize.html via jqeury
    # Output: cumulative return, sharpe, weights
    mlOutput = {}

    context = {
        'df': df,
        'script': script,
        'div': div,
        'stock_dict': stock_dict,
        'mlOutput': mlOutput
    }
    
    return render(request, "homepage.html", context=context)

def compare(request):
    #checkbox for previously saved portfolios (portfolio objects)
    #button to run jquery to display charts and make YoY returns comparison for each portfolio
    #Based on this, safe to say once a portfolio object is created, also need to save their charts and stats to load easily for comparison
   
    all_portfolios = Portfolio.objects.all()


    # Saving output form the checkbox
    try:
        selected_portfolios = request.POST.getlist('checkbox1') # This will show [p_name, p_name, ...]
        df = {'p_name':['Port 1','Port 2'],'sharpe': [1.234,1.5637]} # Dummy data
        #df = ...  #Code to append to selected_portfolios --> {[p_name, sharpe_ratio, volatility], [p_name, sharpe_ratio]}

        context = {
            'selected_portfolios': selected_portfolios
        }
<<<<<<< HEAD

        if selected_portfolios is None:
            return render(request=request, template_name='compare.html', context=context)

=======

        if selected_portfolios is None:
            return render(request=request, template_name='compare.html', context=context)

>>>>>>> 35b52fa5d4754ec5f6167bbd16639f0fa0ec9ad4
        else:
            p = figure(x_range = df['p_name'], plot_height=300, plot_width=1000, title="Portfolio Comparison",
            toolbar_location=None, tools="")
            p.vbar(x = df['p_name'], top = df['sharpe'], width = 0.9, hover_color="pink")
            p.xgrid.grid_line_color = None
            p.ygrid.grid_line_color = None
            p.background_fill_color = None
            p.border_fill_color = None
            p.title.text_font = "gill"
            p.title.text_font_size = "24px"
            p.title.text_color = "white"
            p.yaxis.axis_label = "Sharpe Ratio"
            p.yaxis.axis_label_text_font = "gill"
            p.yaxis.axis_label_text_color = "white"
            p.xaxis.major_label_text_font = "gill"
            p.xaxis.major_label_text_font_size = "20px"
            p.xaxis.major_label_text_font_style = "bold"
            p.xaxis.major_label_text_color = "white"
            p.yaxis.major_label_text_font = "gill"
            p.yaxis.major_label_text_font_size = "20px"
            p.yaxis.major_label_text_color = "white"
            p.yaxis[0].formatter = NumeralTickFormatter(format="0.00")
            p.add_tools(HoverTool(tooltips=[("Portfolio", "@p_name"), ("Sharpe Ratio", "@sharpe")]))

    except KeyError:
        script = None
        div = None
        div1 = None

        context = {}                   
        
    # pie chart

    '''
    from selected_portfolios, find the id --> use it to reference to port_id --> get stock_id & stock_weight --> find stock_name & ticker
    fill the below counter() with stock_name&ticker, stock_weight
    '''

    x = Counter({
    'United States': 157,
    'United Kingdom': 93,
    'Japan': 89,
    'China': 63,
    'Germany': 44,
    'India': 42,
    'Italy': 40,
    'Australia': 35,
    'Brazil': 32,
    'France': 31,
    'Taiwan': 31,
    'Spain': 29
    })

    data = pd.Series(x).reset_index(name='value').rename(columns={'index':'country'})
    data['angle'] = data['value']/sum(x.values()) * 2*pi
    data['color'] = Category20c[len(x)]

    p1 = figure(plot_height=350, plot_width= 470, title="Pie Chart", toolbar_location=None,
            tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

    p1.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='country', source=data, hover_color="pink")

    p1.title.text_font="gill"
    p1.axis.axis_label=None
    p1.axis.visible=False
    p1.grid.grid_line_color = None
    p1.legend.label_text_font="gill"

    script, (div, div1) = components((p, p1))

    context = {
        'script' : script,
        'div' : div, 
        'div1' : div1,
    }
    
    return render(request, "compare.html", context=context)

def optimize(request):
    # Create chart and data table to display in optimized html 

    # Get the output file from ML model in the form of {stock_name, stock_weights}
    # df = read csv???
    
    
    # GRAPHS

    '''
    try:
        df = ...  #Code to append to selected_portfolios --> {[p_name, sharpe_ratio, volatility], [p_name, sharpe_ratio]}
    except KeyError:
        
		script = None
		div = None
	else:
    p = figure(x_range = df['p_name'], plot_height=300, plot_width=500, title="Portfolio Comparison",
            toolbar_location=None, tools="")
    p.vbar(x = df['p_name'], top = df['sharpe'], width = 0.9, hover_color="pink")
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.background_fill_color = None
    p.border_fill_color = None
    p.title.text_font = "gill"
    p.title.text_font_size = "24px"
    p.yaxis.axis_label = "Sharpe Ratio"
    p.yaxis.axis_label_text_font = "gill"
    p.xaxis.major_label_text_font = "gill"
    p.xaxis.major_label_text_font_size = "20px"
    p.xaxis.major_label_text_font_style = "bold"
    p.yaxis.major_label_text_font = "gill"
    p.yaxis.major_label_text_font_size = "20px"
    p.add_tools(HoverTool(tooltips=[("Portfolio", "@p_name"), ("Sharpe Ratio", "@sharpe")]))
    script, div = components(p) #### This will be combined with components(p1)
    
    ###############
    p1 = figure(x_range = df['p_name'], plot_height=300, plot_width=500, title="Portfolio Comparison",
            toolbar_location=None, tools="")
    p1.vbar(x = df['p_name'], top = df['volatility'], width = 0.9, hover_color="pink")
    p1.xgrid.grid_line_color = None
    p1.ygrid.grid_line_color = None
    p1.background_fill_color = None
    p1.border_fill_color = None
    p1.title.text_font = "gill"
    p1.title.text_font_size = "24px"
    p1.yaxis.axis_label = "Sharpe Ratio"
    p1.yaxis.axis_label_text_font = "gill"
    p1.xaxis.major_label_text_font = "gill"
    p1.xaxis.major_label_text_font_size = "20px"
    p1.xaxis.major_label_text_font_style = "bold"
    p1.yaxis.major_label_text_font = "gill"
    p1.yaxis.major_label_text_font_size = "20px"
    p1.add_tools(HoverTool(tooltips=[("Portfolio", "@p_name"), ("Volatility", "@volatility")]))
    
    '''


    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']

    p = figure(x_range=fruits, plot_height=300, plot_width=500, title="Fruit Counts",
            toolbar_location=None, tools="")

    p.vbar(x=fruits, top=[5, 3, 4, 2, 4, 6], width=0.9, hover_color="pink")

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.background_fill_color = None
    p.border_fill_color = None

    p.add_tools(HoverTool(tooltips=[("Fruit", "@fruits"), ("Count", "@y")]))
    
    p.title.text_font = "gill"
    p.title.text_font_size = "24px"
    p.xaxis.major_label_text_font = "gill"
    p.xaxis.major_label_text_font_size = "20px"
    p.yaxis.major_label_text_font = "gill"
    p.yaxis.major_label_text_font_size = "20px"

    ############

    p1 = figure(x_range=fruits, plot_height=300, plot_width=500, title="Fruit Counts",
            toolbar_location=None, tools="")

    p1.vbar(x=fruits, top=[5, 3, 4, 2, 4, 6], width=0.9, hover_color="pink")

    p1.xgrid.grid_line_color = None
    p1.ygrid.grid_line_color = None
    p1.background_fill_color = None
    p1.border_fill_color = None

    p1.add_tools(HoverTool(tooltips=[("Fruit", "@fruits"), ("Count", "@y")]))
    
    p1.title.text_font = "gill"
    p1.title.text_font_size = "24px"
    p1.xaxis.major_label_text_font = "gill"
    p1.xaxis.major_label_text_font_size = "20px"
    p1.yaxis.major_label_text_font = "gill"
    p1.yaxis.major_label_text_font_size = "20px"
    
    # pie chart

    '''
    chart = from df, find the stock_name, stock_weight
    change counter() to stock_name, stock_weight
    '''

    x = Counter({
    'United States': 157,
    'United Kingdom': 93,
    'Japan': 89,
    'China': 63,
    'Germany': 44,
    'India': 42,
    'Italy': 40,
    'Australia': 35,
    'Brazil': 32,
    'France': 31,
    'Taiwan': 31,
    'Spain': 29
    })

    data = pd.Series(x).reset_index(name='value').rename(columns={'index':'country'})
    data['angle'] = data['value']/sum(x.values()) * 2*pi
    data['color'] = Category20c[len(x)]

    p2 = figure(plot_height=350, plot_width= 470, title="Pie Chart", toolbar_location=None,
            tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

    p2.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='country', source=data, hover_color="pink")

    p2.title.text_font="gill"
    p2.axis.axis_label=None
    p2.axis.visible=False
    p2.grid.grid_line_color = None
    p2.legend.label_text_font="gill"

    script, (div, div1, div2) = components((p, p1, p2))

    ''' What happens when user saves a portfolio '''
    # portfolio is a jquery list variable containing a saved portfolio. [0]:portfolio name and [1]:description 
    portfolio = request.POST.get("portfolio")

    # Create portfolio object
    Portfolio.objects.create(p_name=portfolio[0], p_desc=portfolio[1], cum_return='from ml', sharpe='from ml', created_at=datetime.now(), created_by='User.objects.get(id=logged_in_username_id).username') 

    # Create User_Portfolio object
    User_Portfolio.objects.create(user_id='User.objects.get(id=logged_in_username_id).id', portfolio_id='Portfolio.objects.get(id=0).id')

    # Create Portfolio_Stocks object per selected stocks
    for each in selected_stocks:
        Portfolio_Stocks.objects.create(port_id='Portfolio.objects.get(id=0).id', stock_id='Stocks.objects.get(ticker=each).id', stock_weight='from ml')

    ''' Retrieving Portfolio Info for Portfolios page '''
    # for loop to get all user's saved portfolio name and description, using the number of same ids in the database
    for each in User_Portfolio.objects.get(user_id="logged_in_username_id"):
        count = 1
        user_port_dic = {} # to bring user_port_dic to store in front end local storage for future usage
        user_port_dic['portfolio_{}'.format(count)] = {'name':Portfolio.objects.get(id=each).p_name, 'description':Portfolio.objects.get(id=each).p_desc, 'stocks': {'ticker': Stocks.objects.get(id=0).ticker, 'forecasted_returns': Stocks.objects.get(id=0).forecast_return}}
        count += 1

    context = {
        'script' : script,
        'div' : div, 
        'div1' : div1,
        'div2': div2,
        'user_port_dic': user_port_dic
    }

    return render(request, "optimize.html", context=context)

def portfolios(request):
    #listing out of all saved portfolio objects
    #listing out the created_on date for all saved portfolio objects 
    
    portfolios = Portfolio.objects.all()
    port_names = list()
    port_desc = list()
    port_create = list()
    i = 1
    number = []

    for each in portfolios:
        port_names.append(each.p_name)
        port_desc.append(each.p_desc)
        port_create.append(each.created_at)
        number.append(i)
        i += 1
        
    context = {
        'portfolios': portfolios,
        'port_names': port_names,
        'port_desc': port_desc,
        'port_create': port_create,
        'number': number
    }

    return render(request, 'portfolios.html', context=context)

def portfolio_id(request):
    return render(request, 'portfolio1.html')

def create_stocks():
    ''' Create Stocks Objects '''
    stocks_df = pd.read_csv('tickers_latest.csv')
    tup = stocks_df.values
<<<<<<< HEAD

    for each in tup:
        Stocks.objects.create(stock_id=each[0], stock_name=each[2], ticker=each[1], forecast_return=each[3], mse=each[4])
    
    return
    ''' Link front end stocks selection inputs to back-end '''
=======
>>>>>>> 35b52fa5d4754ec5f6167bbd16639f0fa0ec9ad4

    for each in tup:
        Stocks.objects.create(stock_id=each[0], stock_name=each[2], ticker=each[1], forecast_return=each[3], mse=each[4])
    
    return
    ''' Link front end stocks selection inputs to back-end '''