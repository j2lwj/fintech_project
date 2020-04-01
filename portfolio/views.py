from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, QueryDict, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
import requests
import pandas as pd
from datetime import datetime
# from stocks import app, db
# from stocks.models import StockPrice
# from flask import request, jsonify, render_template, Response
from bs4 import BeautifulSoup
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.layouts import widgetbox
from bokeh.embed import components
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from .models import Portfolio, User_Portfolio, Stocks, Portfolio_Stocks
import datetime
from collections import Counter
from math import pi

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
        return render(request, 'homepage.html')
    else:
        return render(request, "login.html")

def signup(request):
    #receive input from form - method=POST, must be unique
    #input type: email, password, text
    #already a member? log in - href to login html
    #inputs: fName, lName, email, password 
    #input submit button, save objects to user
    # https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    #only have log-in button - href to login html 
    return render(request, "main_home.html")

def my_portfolio(request):
    #receive input from form - method=GET from stocks database, inputs: datalist of all stocks in universe
    #add and remove stocks and allocation form button - using jquery
    #output for allocation ((no. of shares x price)/total capital
    #save button - create a new portfolio object
    """
    optimize button - backend ML processing: input - ticker, var1, var2 etc . output - 1) percentage allocation 
    bokeh chart to display line chart (current vs optimized vs bm), 2) pie chart (% allocation), 3) YoY returns
    (current vs optimized) - pie chart using jquery linked to allocation, the rest is backend processing.
    """
    # Create Stocks Objects
    stocks_df = pd.read_csv('sector10_tickers.csv')
    tup = stocks_df.values
    
    # for each in tup:
    #     Stocks.objects.create(stock_id=each[0], stock_name=each[2], ticker=each[1], created_at=datetime.datetime.now())
    
    lis = []
    for each in tup:
        lis.append(each[1])
        lis.append(each[2])
    
    lis = ['AMOCO CORP (AN.2)', 'ANDEAVOR (ANDV)', 'ALPHA NATURAL RESOURCES INC (ANRZQ)', 'APACHE CORP (APA)', 'ANADARKO PETROLEUM CORP (APC)', 'ATLANTIC RICHFIELD CO (ARC.3)', 'BAKER HUGHES INC (BHI)', 'BJ SERVICES CO (BJS.1)', 'BURLINGTON RESOURCES INC (BR.2)', 'PEABODY ENERGY CORP (BTU)', 'CAMERON INTERNATIONAL CORP (CAM)', 'CHESAPEAKE ENERGY CORP (CHK)', 'CONSOL ENERGY INC (CNX)', 'CONOCO INC (COC1)', 'CABOT OIL & GAS CORP (COG)', 'CONOCOPHILLIPS (COP)', 'COLUMBIA PIPELINE GROUP INC (CPGX)', 'CHEVRON CORP (CVX)', 'CONCHO RESOURCES INC (CXO)', 'DRESSER INDUSTRIES INC (DI.)', 'DENBURY RESOURCES INC (DNR)', 'DIAMOND OFFSHRE DRILLING INC (DO)', 'DEVON ENERGY CORP (DVN)', 'EOG RESOURCES INC (EOG)', 'EL PASO CORP (EP)', 'EQT CORP (EQT)', 'ENSCO PLC (ESV)', 'TECHNIPFMC PLC (FTI)', 'FMC TECHNOLOGIES INC (FTI.1)', 'HALLIBURTON CO (HAL)', 'HESS CORP (HES)', 'HELMERICH & PAYNE (HP)', 'KERR-MCGEE CORP (KMG.1)', 'KINDER MORGAN INC (KMI)', 'LOUISIANA LAND & EXPLORATION (LLX.)', 'MCDERMOTT INTL INC (MDR)', 'MASSEY ENERGY CO (MEE)', 'MOBIL CORP (MOB.2)', 'MARATHON PETROLEUM CORP (MPC)', 'MARATHON OIL CORP (MRO)', 'USX CORP-CONSOLIDATED (MROX.CM)', 'MURPHY OIL CORP (MUR)', 'MAXUS ENERGY CORP (MXS)', 'NOBLE ENERGY INC (NBL)', 'NABORS INDUSTRIES LTD (NBR)', 'NACCO INDUSTRIES  -CL A (NC)', 'NOBLE CORP PLC (NE)', 'NEWFIELD EXPLORATION CO (NFX)', 'NATIONAL OILWELL VARCO INC (NOV)', 'ONEOK INC (OKE)', 'ORYX ENERGY CO (ORX)', 'OCCIDENTAL PETROLEUM CORP (OXY)', 'PHILLIPS 66 (PSX)', 'PIONEER NATURAL RESOURCES CO (PXD)', 'PENNZENERGY CO (PZE.1)', 'QEP RESOURCES INC (QEP)', 'ROWAN COMPANIES PLC (RDC)', 'ROYAL DUTCH PETROLEUM NV (RDPL)', 'TRANSOCEAN LTD (RIG)', 'RANGE RESOURCES CORP (RRC)', 'SANTA FE SNYDER CORP (SFS.1)', 'SMITH INTERNATIONAL INC (SII)', 'SCHLUMBERGER LTD (SLB)', 'SUNOCO INC (SUN.1)', 'SOUTHWESTERN ENERGY CO (SWN)', 'STEEL EXCEL INC (SXCL)', 'TOSCO CORP (TOS.1)', 'TEXACO INC (TX.2)', 'UNOCAL CORP (UCL)', 'UNION PACIFIC RESOURCES GRP (UPR.1)', 'VALERO ENERGY CORP (VLO)', 'WESTERN ATLAS INC (WAI.1)', 'WEATHERFORD INTL PLC (WFT)', 'WESTMORELAND COAL CO (WLB)', 'WILLIAMS COS INC (WMB)', 'WPX ENERGY INC (WPX)', 'CIMAREX ENERGY CO (XEC)', 'EXXON MOBIL CORP (XOM)', 'XTO ENERGY INC (XTO)']
    
    # Based on front-end user input in forms, back end create portfolio
    # When user clicks on "save" button, form pop-up --> https://www.w3schools.com/howto/howto_js_popup_form.asp
    p_name = request.GET.get('p_name')
    p_desc = request.GET.get('p_desc') 
    stocks = request.GET.get('stock_array') 

    context = {
        'p_name': p_name,
        'p_desc': p_desc,
        'stocks': stocks,
        'lis': lis
    }
    
    return render(request, "homepage.html", context=context)

def compare(request):
    #checkbox for previously saved portfolios (portfolio objects)
    #button to run jquery to display charts and make YoY returns comparison for each portfolio
    #Based on this, safe to say once a portfolio object is created, also need to save their charts and stats to load easily for comparison
    # all_portfolios = Portfolio.objects.all()

    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']

    p = figure(x_range=fruits, plot_height=300, plot_width=1000, title="Fruit Counts",
            toolbar_location=None, tools="")

    p.vbar(x=fruits, top=[5, 3, 4, 2, 4, 6], width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0


    # pie chart
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
            line_color="white", fill_color='color', legend='country', source=data)

    p1.axis.axis_label=None
    p1.axis.visible=False
    p1.grid.grid_line_color = None

    script, (div, div1) = components((p, p1))


    context = {
        'script' : script,
        'div' : div, 
        'div1' : div1
    }
    
    return render(request, "compare.html", context=context)

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


# def live_price(request):

# 	ticker = request.GET.get('ticker', None)
# 	context_data = {'ticker' : ticker}
# 	if ticker is None:
# 		return render(request=request, template_name='live_price.html', context=context_data)

# 	url = 'http://quotes.wsj.com/{}'.format(ticker)
# 	# https://www.wsj.com/market-data/quotes/AAPL
# 	r = requests.get('https://www.wsj.com/market-data/quotes/AAPL')
# 	soup = BeautifulSoup(r.content, 'html.parser')
# 	return HttpResponse(content=r.text, content_type="text/html")
# 	try:
# 		realtime_price_el = soup.find('span', attrs={'id': 'quote_val'})
# 		return HttpResponse(content=realtime_price_el, content_type="application/json")
# 		range_el = soup.find('ul', attrs={'class': 'cr_charts_info'})\
# 					.find_all('li')[2]\
# 					.find('span', attrs={'class': 'data_data'})
# 	except AttributeError:
# 		realtime_price = None
# 		open_price = None
# 		close_price = None
# 	else:
# 		if realtime_price_el is not None:
# 			realtime_price = float(realtime_price_el.text.replace(',', ''))
# 		else:
# 			realtime_price = None
# 		if range_el is not None:
# 			prices = range_el.text.split(' - ')
# 			open_price = float(prices[0].replace(',', ''))
# 			close_price = float(prices[1].replace(',', ''))
# 		else:
# 			open_price = None
# 			close_price = None

# 		prices = StockPrice(ticker=ticker.upper(), open_price=open_price, close_price=close_price, realtime_price=realtime_price, created_at=datetime.now())
# 		# db.session.add(prices)
# 		# db.session.commit()
# 	context = {
# 			'ticker' : ticker.upper(),
# 			'open_price' : open_price,
# 			'close_price' : close_price,
# 			'realtime_price' : realtime_price
# 		}
# 	return render(request=request , template_name='live_price.html', context=context)

# def trading_volume(request):
    	
# 	# return HttpResponse(content=request.GET.get, content_type="application/json")
# 	# ticker = None if request.GET['ticker'] == None else request.GET['ticker']
# 	ticker = request.GET.get('ticker', '')
# 	# time_range = None if request.GET['range'] == None else request.GET['range']
# 	time_range = request.GET.get('range', '')
# 	time_range_options = ["Daily", "Weekly", "Monthly"]
	
# 	context = {
#         'ticker' : ticker,
#         'time_range' : time_range,
#         'time_range_options' : time_range_options,
#     }

# 	if ticker is None or time_range is None:
#     		return render(request=request, template_name='trading_volume.html', context=context)

# 	url = 'https://www.alphavantage.co/query?function=TIME_SERIES_{}&symbol={}&apikey=6IPKGXBQSR1WLQUK'.format(time_range.upper(), ticker.upper())
# 	res = requests.get(url)
# 	data = res.json()
	
# 	key_dict = {
# 		"Daily" : "Time Series (Daily)",
# 		"Weekly" : "Weekly Time Series",
# 		"Monthly" : "Monthly Time Series",
# 	}

# 	try:
# 		df = pd.DataFrame.from_dict(data[key_dict[time_range]], orient='index')
# 	except KeyError:
# 		script = None
# 		div = None
# 		time_range = None
# 	else:
# 		df['date'] = pd.to_datetime(df.index)
# 		source = ColumnDataSource(data=df)

# 		ticker = ticker.upper()
# 		p = figure(plot_width=800, plot_height=500, x_axis_type="datetime")
# 		p.title.text = "{} Trading Volume for {}".format(time_range, ticker)
# 		p.line(x='date', y='5. volume', source=source)
# 		p.yaxis[0].formatter = NumeralTickFormatter(format="0.0a")

# 		script, div = components(p)

# 		context = {
# 			'script' : script,
# 			'div' : div, 
# 			'ticker' : ticker, 
# 			'time_range' : time_range,
# 			'time_range_options' : time_range_options
# 		}

# 	return render(request=request, template_name='trading_volume.html', context=context)

# def price_history(request):
    
# 	query = StockPrice.objects.all()

# 	# return HttpResponse(content=query[0].ticker, content_type='text/html')

# 	df = pd.DataFrame(data=query)
# 	# df = pd.read_sql(query.statement, query.session.bind)
# 	# df.sort_values('created_at', ascending=False, inplace=True)
# 	source = ColumnDataSource(df)

# 	columns = [
# 	        # TableColumn(field="created_at", title="Created At", formatter=DateFormatter(format="%F %T")),
# 	        TableColumn(field="ticker", title="Ticker"),
# 	        TableColumn(field="open_price", title="Open Price"),
# 	        TableColumn(field="close_price", title="Close Price"),
# 	        TableColumn(field="realtime_price", title="Real Time Price"),
# 	    ]
# 	data_table = DataTable(source=source, columns=columns, width=800, height=280)
# 	script, div = components(widgetbox(data_table))

# 	context_data = {
# 		'script' : script,
# 		'div'	 : div
# 	}
# 	return render(request=request, template_name='price_history.html', context=context_data)

# def price_json(request):
# 	ticker = request.GET.get('ticker', None)
# 	if ticker is None:
# 		return "No ticker provided"

# 	res = {}

# 	# scrape website
# 	r = requests.get('http://quotes.wsj.com/{}'.format(ticker))
# 	soup = BeautifulSoup(r.content, 'html.parser')

# 	real_time_el = soup.find('span', attrs={'id': 'quote_val'})
	
# 	range_el = soup.find('ul', attrs={'class': 'cr_charts_info'})\
# 				.find_all('li')[2]\
# 				.find('span', attrs={'class': 'data_data'})

# 	if real_time_el is not None:
# 		res['real_time'] = float(real_time_el.text)
# 	else:
# 		res['real_time'] = None
# 	if range_el is not None:
# 		prices = range_el.text.split(' - ')
# 		res['open_price'] = float(prices[0])
# 		res['close_price'] = float(prices[1])
# 	else:
# 		res['open_price'] = None
# 		res['close_price'] = None

# 	return JsonResponse(res)