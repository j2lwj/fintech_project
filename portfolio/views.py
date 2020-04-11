# Django Library
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, QueryDict, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm

# Python Library
import requests
import datetime
import pandas as pd
from datetime import datetime
from collections import Counter
from math import pi
from bs4 import BeautifulSoup

# Bokeh Libraries
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.layouts import widgetbox
from bokeh.embed import components
from bokeh.palettes import Category20c
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

    # GRAPHS
    
    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']

    p = figure(x_range=fruits, plot_height=300, plot_width=1000, title="Fruit Counts",
            toolbar_location=None, tools="")

    p.vbar(x=fruits, top=[5, 3, 4, 2, 4, 6], width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    script, div = components(p)
    
    '''
    Work-In-Progress: linking the 'Forecast' button to the variables in 'p'

    stocks = request.POST.get("array of stocks")
    
    #Run the ML backend model to get the forecasted returns of each stock
    
	try:

        df = "retrieve the data from the ML model as a dictionary"

    except KeyError:
        
		script = None
		div = None

	else:

    p = figure(x_range = df[stock_name], plot_height=300, plot_width=1000, title="Next Quarter Forecasted Returns",
            toolbar_location=None, tools="")

    p.vbar(x = df['stock_name'], top = df['stock_weight'], width = 0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    script, div = components(p)
    '''
    # Create Stocks Objects

    stocks_df = pd.read_csv('tickers.csv')
    tup = stocks_df.values
    lis = []

    for each in tup:
        Stocks.objects.create(stock_id=each[0], stock_name=each[2], ticker=each[1], created_at=datetime.datetime.now())
        # stock = "{} ({})".format(each[2], each[1])
        # lis.append(stock)
    
    for each in Stocks.objects.all():
        stock = "{} ({})".format(each.stock_name, each.ticker)
    # print(lis)
    # lis = ['HARTFORD FICIAL SERVICES (HIG)', 'LAUDER (ESTEE) COS INC -CL A (EL)', 'LINCOLN NATIONAL CORP (LNC)', 'HUMANA INC (HUM)', 'GRAINGER (W W) INC (GWW)', 'INCYTE CORP (INCY)', 'DELUXE CORP (DLX)', 'ENTERGY CORP (ETR)', 'GRACE (W R) & CO (GRA)', 'PRINCIPAL FICIAL GRP INC (PFG)', 'PRUDENTIAL FICIAL INC (PRU)', 'AVON PRODUCTS (AVP)', 'METLIFE INC (MET)', 'SKYLINE CORP (SKY)', 'AMERISOURCEBERGEN CORP (ABC)', 'AK STEEL HOLDING CORP (AKS)', 'BROADVISION INC (BVSN)', 'ORACLE CORP (ORCL)', 'SNAP-ON INC (SNA)', 'ALPHABET INC (GOOGL)', 'MONSTER BEVERAGE CORP (MNST)', 'SYSCO CORP (SYY)', 'CNA FICIAL CORP (CNA)', 'NEWFIELD EXPLORATION CO (NFX)', 'UNITED STATES STEEL CORP (X)', 'LOUISIANA-PACIFIC CORP (LPX)', 'MGIC INVESTMENT CORP/WI (MTG)', 'AETNA INC (AET)', 'JACOBS ENGINEERING GROUP INC (JEC)', 'XL GROUP LTD (XL)', 'BLOCK H & R INC (HRB)', 'ADOBE SYSTEMS INC (ADBE)', 'ALASKA AIR GROUP INC (ALK)', 'ANSYS INC (ANSS)', 'ANTHEM INC (ANTM)', 'CHESAPEAKE ENERGY CORP (CHK)', 'HOST HOTELS & RESORTS INC (HST)', 'IAC/INTERACTIVECORP (IAC)', 'KB HOME (KBH)', 'MCKESSON CORP (MCK)', 'PAYCHEX INC (PAYX)', 'BRIGGS & STRATTON (BGG)', 'CRANE CO (CR)', 'DEVON ENERGY CORP (DVN)', 'EBAY INC (EBAY)', 'IRON MOUNTAIN INC (IRM)', 'LENNAR CORP (LEN)', 'ROBERT HALF INTL INC (RHI)', 'UNITEDHEALTH GROUP INC (UNH)', 'COCA-COLA EUROPEAN PARTNERS (CCE)', 'PENNEY (J C) CO (JCP)', 'OFFICE DEPOT INC (ODP)', 'PULTEGROUP INC (PHM)', 'VERTEX PHARMACEUTICALS INC (VRTX)', 'BRINKS CO (BCO)', 'COGNIZANT TECH SOLUTIONS (CTSH)', 'SEARS HOLDINGS CORP (SHLD)', 'USG CORP (USG)', 'WESTROCK CO (WRK)', 'WELLTOWER INC (HCN)', 'LUBYS INC (LUB)', 'APPLE INC (AAPL)', 'AKAMAI TECHNOLOGIES INC (AKAM)', 'ABERCROMBIE & FITCH  -CL A (ANF)', 'CALERES INC (CAL)', 'JUNIPER NETWORKS INC (JNPR)', 'NORTHROP GRUMMAN CORP (NOC)', 'NUCOR CORP (NUE)', 'APACHE CORP (APA)', 'BASSETT FURNITURE INDS (BSET)', 'CMS ENERGY CORP (CMS)', 'DUN & BRADSTREET CORP (DNB)', 'DAVITA INC (DVA)', 'HELMERICH & PAYNE (HP)', 'MBIA INC (MBI)', 'MGM RESORTS INTERNATIONAL (MGM)', 'NRG ENERGY INC (NRG)', 'QUALCOMM INC (QCOM)', 'UNUM GROUP (UNM)', 'BEST BUY CO INC (BBY)', 'CHUBB LTD (CB)', 'DENBURY RESOURCES INC (DNR)', 'NETFLIX INC (NFLX)', 'TIMKEN CO (TKR)', 'UNIVERSAL HEALTH SVCS INC (UHS)', 'FEDEX CORP (FDX)', 'GLOBAL PAYMENTS INC (GPN)', 'ROYAL CARIBBEAN CRUISES LTD (RCL)', 'SHERWIN-WILLIAMS CO (SHW)', 'AUTODESK INC (ADSK)', 'CA INC (CA)', 'CBRE GROUP INC (CBG)', 'DUKE ENERGY CORP (DUK)', 'GOODYEAR TIRE & RUBBER CO (GT)', 'KIMCO REALTY CORP (KIM)', 'NABORS INDUSTRIES LTD (NBR)', 'NACCO INDUSTRIES  -CL A (NC)', 'PRICELINE GROUP INC (PCLN)', 'SEALED AIR CORP (SEE)', 'TENET HEALTHCARE CORP (THC)', 'TIFFANY & CO (TIF)', 'AMERIPRISE FICIAL INC (AMP)', 'CENTURYLINK INC (CTL)', 'CONVERGYS CORP (CVG)', 'ENVISION HEALTHCARE CORP (EVHC)', 'GGP INC (GGP)', 'HOLOGIC INC (HOLX)', 'RANGE RESOURCES CORP (RRC)', 'AMEREN CORP (AEE)', 'ASSURANT INC (AIZ)', 'ALLSTATE CORP (ALL)', 'BOSTON SCIENTIFIC CORP (BSX)', 'CARDINAL HEALTH INC (CAH)', 'CINCINNATI FICIAL CORP (CINF)', 'GRAHAM HOLDINGS CO (GHC)', 'GENWORTH FICIAL INC (GNW)', 'MCDERMOTT INTL INC (MDR)', 'MORGAN STANLEY (MS)', 'NORTHERN TRUST CORP (NTRS)', 'PIONEER NATURAL RESOURCES CO (PXD)', 'RAYTHEON CO (RTN)', 'SANMINA CORP (SANM)', 'SUNEDISON INC (SUNEQ)', 'UNITED RENTALS INC (URI)', 'VIAVI SOLUTIONS INC (VIAV)', 'VALERO ENERGY CORP (VLO)', 'WORTHINGTON INDUSTRIES (WOR)', 'ALTABA INC (AABA)', 'AES CORP (AES)', 'ALLEGHENY TECHNOLOGIES INC (ATI)', 'DDR CORP (DDR)', 'DEAN FOODS CO (DF)', 'ELECTRONIC ARTS INC (EA)', 'EQUIFAX INC (EFX)', 'GENESCO INC (GCO)', 'MATTEL INC (MAT)', 'NETAPP INC (NTAP)', 'ONEOK INC (OKE)', 'MOLSON COORS BREWING CO (TAP)', 'TJX COMPANIES INC (TJX)', 'UNISYS CORP (UIS)', 'AMERICAN ELECTRIC POWER CO (AEP)', 'ADTALEM GLOBAL EDUCATION INC (ATGE)', 'DILLARDS INC  -CL A (DDS)', 'D R HORTON INC (DHI)', 'DISH NETWORK CORP (DISH)', 'EOG RESOURCES INC (EOG)', 'GENERAL DYNAMICS CORP (GD)', 'HCP INC (HCP)', 'HORMEL FOODS CORP (HRL)', 'MACERICH CO (MAC)', "MOODY'S CORP (MCO)", 'NORFOLK SOUTHERN CORP (NSC)', 'EVEREST RE GROUP LTD (RE)', 'REGENERON PHARMACEUTICALS (REGN)', 'SCANA CORP (SCG)', 'TOTAL SYSTEM SERVICES INC (TSS)', 'YUM BRANDS INC (YUM)', 'ARCHER-DANIELS-MIDLAND CO (ADM)', 'AMAZON.COM INC (AMZN)', 'ANADARKO PETROLEUM CORP (APC)', 'BROWN FORMAN CORP (BF.B)', 'CINTAS CORP (CTAS)', 'DARDEN RESTAURANTS INC (DRI)', 'GOLDMAN SACHS GROUP INC (GS)', 'HEALTHSOUTH CORP (HLS)', 'MARATHON OIL CORP (MRO)', 'NEW YORK TIMES CO  -CL A (NYT)', 'REALTY INCOME CORP (O)', 'OWENS-ILLINOIS INC (OI)', 'PERKINELMER INC (PKI)', 'PVH CORP (PVH)', 'REPUBLIC SERVICES INC (RSG)', 'SOUTHERN CO (SO)', 'TEXTRON INC (TXT)', 'CIMAREX ENERGY CO (XEC)', 'YRC WORLDWIDE INC (YRCW)', 'ACCENTURE PLC (ACN)', 'ALLIANCE DATA SYSTEMS CORP (ADS)', 'ALEXION PHARMACEUTICALS INC (ALXN)', 'ASHLAND GLOBAL HOLDINGS INC (ASH)', 'BERKSHIRE HATHAWAY (BRK.B)', 'CENTENE CORP (CNC)', 'EDISON INTERNATIONAL (EIX)', 'EQUINIX INC (EQIX)', 'INTERPUBLIC GROUP OF COS (IPG)', 'SOUTHWEST AIRLINES (LUV)', 'MICROSOFT CORP (MSFT)', 'NAVIENT CORP (NAVI)', 'PG&E CORP (PCG)', 'ROSS STORES INC (ROST)', 'THERMO FISHER SCIENTIFIC INC (TMO)', 'ZIONS BANCORPORATION (ZION)']
   
    # Link front end stocks selection inputs to back-end
    
    
    # return forecasted returns of selected in graph form



    ''' For Optimization Page '''
    # Based on front-end user input in forms, back end create portfolio

    p_name = request.GET.get('p_name')
    p_desc = request.GET.get('p_desc') 
    stocks = request.GET.get('stock_array') 

    # Create and Save portfolio objects into Portfolio database

    Portfolio.objects.create(p_name=p_name, p_desc=p_desc, cum_return= , cagr= , sharpe= , max_drawdown= , created_by=user) 
    
    context = {
        'p_name': p_name,
        'p_desc': p_desc,
        'stocks': stocks,
        'lis': lis,
        'script': script,
        'div': div,
    }
    
    return render(request, "homepage.html", context=context)

def compare(request):
    #checkbox for previously saved portfolios (portfolio objects)
    #button to run jquery to display charts and make YoY returns comparison for each portfolio
    #Based on this, safe to say once a portfolio object is created, also need to save their charts and stats to load easily for comparison
   
    # all_portfolios = Portfolio.objects.all()


    # Saving output form the checkbox
    try:

        selected_portfolios = request.POST.getlist('checkbox1') # This will show [p_name, p_name, ...]

    except KeyError:

        script = None
        div = None
        div1 = None

        context = {}                   
    
    # GRAPHS

    '''
    try:

        df = ...  #Code to append to selected_portfolios --> {[p_name, sharpe_ratio, volatility], [p_name, sharpe_ratio]}

    except KeyError:
        
		script = None
		div = None

	else:

    p = figure(x_range = df['p_name'], plot_height=300, plot_width=1000, title="Portfolio Comparison",
            toolbar_location=None, tools="")

    p.vbar(x = df['p_name'], top = df['sharpe_ratio'], width = 0.9, hover_color="pink")

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.background_fill_color = None
    p.border_fill_color = None

    p.title.text_font = "gill"
    p.title.text_font_size = "24px"
    p.title.text_color = "white"
    p.yaxis.axis_label = "Sharpe Ratio"
    p.yaxis.axis_label_text_font = "gill"
    p.yaxis.axis_label_text_font_color = "white"
    p.xaxis.major_label_text_font = "gill"
    p.xaxis.major_label_text_font_size = "20px"
    p.xaxis.major_label_text_font_style = "bold"
    p.xaxis.major_label_text_color = "white"
    p.yaxis.major_label_text_font = "gill"
    p.yaxis.major_label_text_font_size = "20px"
    p.yaxis.major_label_text_color = "white"

    p.add_tools(HoverTool(tooltips=[("Portfolio", "@p_name"), ("Sharpe Ratio", "@sharpe_ratio")]))

    script, div = components(p) #### This will be combined with components(p1)
    
    '''


    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']

    p = figure(x_range=fruits, plot_height=300, plot_width=1000, title="Fruit Counts",
            toolbar_location=None, tools="")

    p.vbar(x=fruits, top=[5, 3, 4, 2, 4, 6], width=0.9, hover_color="pink")

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.background_fill_color = None
    p.border_fill_color = None

    p.add_tools(HoverTool(tooltips=[("Fruit", "@fruits"), ("Count", "@y")]))
    
    p.title.text_font = "gill"
    p.title.text_font_size = "24px"
    p.title.text_color = "white"
    p.xaxis.major_label_text_font = "gill"
    p.xaxis.major_label_text_font_size = "20px"
    p.xaxis.major_label_text_color = "white"
    p.yaxis.major_label_text_font = "gill"
    p.yaxis.major_label_text_font_size = "20px"
    p.yaxis.major_label_text_color = "white"
    
    # pie chart

    '''
    jkhashjkasjhkas
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
        'selected_portfolios': selected_portfolios
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