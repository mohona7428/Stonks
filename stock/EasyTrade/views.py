from logging import _STYLES
from types import LambdaType
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from matplotlib import figure
# from django.http import HttpResponse
import requests
import json
import pandas as pd
import pandas_datareader as data
from datetime import date

# from tensorflow.python.eager import context
from .models import Stock
from .forms import StockForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,  login, logout
from .models import *
from nsepython import *
# Create your views here.


def index(request):
    from bsedata.bse import BSE
    b = BSE()
    gainer = b.topGainers()
    loser = b.topLosers()
    
    n50name = nse_get_index_quote('NIFTY 50')['indexName']
    n50lastPrice = nse_get_index_quote('NIFTY 50')['last']
    n50_change = float(nse_get_index_quote('NIFTY 50')['last'].replace(",", "")) * float(nse_get_index_quote('NIFTY 50')['percChange'])/100
    n50lastchange = round(n50_change,2)
    n50lastpChange = nse_get_index_quote('NIFTY 50')['percChange']
    nbname = nse_get_index_quote('NIFTY BANK')['indexName']
    nblastPrice = nse_get_index_quote('NIFTY BANK')['last']
    nb_change = float(nse_get_index_quote('NIFTY BANK')['last'].replace(",", "")) * float(nse_get_index_quote('NIFTY BANK')['percChange'])/100
    nblastchange = round(nb_change,2)
    nblastpChange = nse_get_index_quote('NIFTY BANK')['percChange']
    niname = nse_get_index_quote('NIFTY IT')['indexName']
    nilastPrice = nse_get_index_quote('NIFTY IT')['last']
    ni_change = float(nse_get_index_quote('NIFTY IT')['last'].replace(",", "")) * float(nse_get_index_quote('NIFTY IT')['percChange'])/100
    nilastchange = round(ni_change,2)
    nilastpChange = nse_get_index_quote('NIFTY IT')['percChange']
    nnname = nse_get_index_quote('NIFTY NEXT 50')['indexName']
    nnlastPrice = nse_get_index_quote('NIFTY NEXT 50')['last']
    nn_change = float(nse_get_index_quote('NIFTY NEXT 50')['last'].replace(",", "")) * float(nse_get_index_quote('NIFTY NEXT 50')['percChange'])/100
    nnlastchange = round(nn_change,2)
    nnlastpChange = nse_get_index_quote('NIFTY NEXT 50')['percChange']
    # for t in gainer:
    #     diff1 = t["ltp"]-t["previousPrice"]
    #     diff1 = round(diff1, 2)
    #     t.update({'inrdiff': diff1})

    # for i in loser:
    #     diff = i["previousPrice"] - i["ltp"]
    #     diff = round(diff, 2)
    #     i.update({'inrdiff': diff})

    context = {
        'gainer': gainer,
        'loser': loser,
        'n50name': n50name,
        'n50lastPrice': n50lastPrice,
        'n50lastchange': n50lastchange,
        'n50lastpChange': n50lastpChange,
        'nbname': nbname,
        'nblastPrice': nblastPrice,
        'nblastchange': nblastchange,
        'nblastpChange': nblastpChange,
        'niname': niname,
        'nilastPrice': nilastPrice,
        'nilastchange': nilastchange,
        'nilastpChange': nilastpChange,
        'nnname': nnname,
        'nnlastPrice': nnlastPrice,
        'nnlastchange': nnlastchange,
        'nnlastpChange': nnlastpChange,
    }
    return render(request, 'index.html', context)


def prices(request):

    import requests
    import json
    from nsepython import nse_eq
    import plotly.graph_objects as go
    from plotly.offline import plot
    from datetime import date, datetime

    if request.method == "POST":
        ticker = request.POST["ticker"]
        
        data_nse = nse_eq(ticker)
        companyName = data_nse["info"]["companyName"]
        lastPrice = data_nse["priceInfo"]["lastPrice"]
        dayHigh = data_nse["priceInfo"]['intraDayHighLow']['max']
        dayLow = data_nse["priceInfo"]['intraDayHighLow']['min']
        high52 = data_nse["priceInfo"]['weekHighLow']['max']
        low52  = data_nse["priceInfo"]['weekHighLow']['min']
        previousClose = data_nse["priceInfo"]["previousClose"]
        open = data_nse["priceInfo"]["open"]
        pChange = data_nse["priceInfo"]["pChange"]
        change = data_nse["priceInfo"]["change"]
        totalTradedVolume = data_nse['preOpenMarket']['totalTradedVolume']
        
        symbol = data_nse['info']['symbol']
        industry = data_nse['metadata']['industry']
        sector = data_nse['industryInfo']['sector']
        founded = data_nse['metadata']['listingDate']

        # plotly graph

        def candlestick():
            import yfinance as yf
            # Data viz
            import plotly.graph_objs as go
            # Interval required 1 minute
            data = yf.download(tickers=ticker+'.NS',
                               period='1d', interval='1m')
            # declare figure
            fig = go.Figure()
            # Candlestick
            fig.add_trace(go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'], name='market data'))
            # Add titles
            fig.update_layout(
                title='Candlestick Chart',
                yaxis_title='Stock Price (INR per Shares)')
            # X-Axes
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list([
                        dict(count=15, label="15m",
                             step="minute", stepmode="backward"),
                        dict(count=45, label="45m",
                             step="minute", stepmode="backward"),
                        dict(count=1, label="HTD",
                             step="hour", stepmode="todate"),
                        dict(count=3, label="3h", step="hour",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                )
            )
            candlestick_div = plot(fig, output_type='div')
            return candlestick_div
        

        # def heatmap():

        #    import calendar
        #    import jugaad_data.nse as nse
        #    import plotly.express as px

        #    stock = nse.stock_df(symbol=ticker, from_date=date(2012,8,1), to_date=datetime.now().date())
        #    stock['M'] = stock['DATE'].dt.month
        #    stock['Y'] = stock['DATE'].dt.year


        #    stock.sort_values('DATE', inplace=True)
        #    stock.reset_index(drop=True, inplace=True)
        #    stock.set_index('DATE', inplace=True)
        #    stock_monthly = stock.resample("M").last()
        #    stock_monthly['Returns'] = (stock_monthly['CLOSE'] - stock_monthly['CLOSE'].shift(1))*100/stock_monthly['CLOSE'].shift(1)
        #    heatmap_ret = pd.pivot_table(stock_monthly, index='Y', columns='M', values=['Returns'])
        #    a1 = heatmap_ret.__array__()
        #    heatmap_ret.columns = [calendar.month_name[i] for i in range(1,13) ]
        #    fig1 = px.imshow(a1,
        #                     labels=dict(x="Months", y="Year", color="Performance"),
        #                     x=heatmap_ret.columns,
        #                     y=['2021','2020','2019','2018','2017','2016','2015','2014','2013','2012'],
        #                     title="Heatmap of "+ticker
        #                 )
        #    fig1.update_xaxes(side="top")
        #    heatmap_div = plot(fig1, output_type='div')
        #    return heatmap_div

    
    context = {
        'candlestick': candlestick(),
        # 'heatmap':heatmap(),
        'companyName': companyName,
        'lastPrice': lastPrice,
        'dayHigh': dayHigh,
        'dayLow': dayLow,
        'high52': high52,
        'low52': low52,
        'previousClose': previousClose,
        'open': open,
        'pChange': pChange,
        'change': change,
        'totalTradedVolume': totalTradedVolume,
        'symbol':symbol,
        'industry':industry,
        'sector':sector,
        'founded':founded,

    }

    return render(request, 'prices.html', context)
    # else:
    #     return render(request, 'prices.html', {'ticker': "Enter a Ticker symbol above"})


def add_stock(request):
    uname = request.user
    name = uname.username
    if request.method == "POST":
        stock = Stock()
        username = name
        ticker = request.POST.get('ticker')
        stock.uname = username
        stock.ticker = ticker
        stock.save()
        return redirect('add_stock')

    else:
        from nsepython import nse_eq
        data = Stock.objects.filter(uname=name)
        companyName, lastPrice, dayHigh, dayLow = [], [], [], []
        previousClose, open, pChange, change = [], [], [], []

        for i in data:
            sname = i.ticker
            data_nse = nse_eq(sname)
            if 'info' in data_nse:
                companyName.append(data_nse['info']['symbol'])
                lastPrice.append(data_nse["priceInfo"]["lastPrice"])
                dayHigh.append(data_nse["priceInfo"]["intraDayHighLow"]["max"])
                dayLow.append(data_nse["priceInfo"]["intraDayHighLow"]["min"])
                previousClose.append(data_nse["priceInfo"]["previousClose"])
                open.append(data_nse["priceInfo"]["open"])
                pChange.append(round(data_nse["priceInfo"]["pChange"], 2))
                change.append(round(data_nse["priceInfo"]["change"], 2))
            else:
                continue

        context = {
            'companyName': companyName,
            'lastPrice': lastPrice,
            'dayHigh': dayHigh,
            'dayLow': dayLow,
            'previousClose': previousClose,
            'open': open,
            'pChange': pChange,
            'change': change,
            'data': data,
            # 'ticker':ticker,
        }

    return render(request, 'add_stock.html', context)


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    return redirect(delete_stock)


def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})


def about(request):
    messages.success(request, "welcome to about page")
    return render(request, 'about.html')


def desc(request):
    return render(request, 'desc.html')


def desc2(request):
    return render(request, 'desc2.html')


# def dtree(request):
#     return render(request, 'dtree.html')

def contact(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact.name = name
        contact.email = email
        contact.phone = phone
        contact.desc = desc
        contact.save()
        messages.success(
            request, " Your query has been successfully submitted")
    return render(request, 'contact.html')

# def prediction(request):
#     return render(request,'prediction.html')


def index_learn(request):
    return render(request, 'index_learn.html')


def intro_stock_market(request):
    return render(request, 'intro_stock_market.html')


def fundamental_analysis(request):
    return render(request, 'fundamental_analysis.html')


def technical_analysis(request):
    return render(request, 'technical_analysis.html')


def the_need_to_invest(request):
    return render(request, 'the_need_to_invest.html')


def regulators(request):
    return render(request, 'regulators.html')


def ipo_market(request):
    return render(request, 'ipo_market.html')


def the_stock_markets(request):
    return render(request, 'the_stock_markets.html')


def jargons(request):
    return render(request, 'jargons.html')


def clearing_and_settlement(request):
    return render(request, 'clearing_and_settlement.html')


def corporate_actions(request):
    return render(request, 'corporate_actions.html')


def intro_fund_analy(request):
    return render(request, 'intro_fund_analy.html')


def mindset_investor(request):
    return render(request, 'mindset_investor.html')


def read_annual_report(request):
    return render(request, 'read_annual_report.html')


def understanding_p_l_1(request):
    return render(request, 'understanding_p_l_1.html')


def understanding_p_l_2(request):
    return render(request, 'understanding_p_l_2.html')


def understanding_bal_sheet_1(request):
    return render(request, 'understanding_bal_sheet_1.html')


def understanding_bal_sheet_2(request):
    return render(request, 'understanding_bal_sheet_2.html')


def cashflow_statement(request):
    return render(request, 'cashflow_statement.html')


def background(request):
    return render(request, 'background.html')


def introducing_tech_analysis(request):
    return render(request, 'introducing_tech_analysis.html')


def chart_types(request):
    return render(request, 'chart_types.html')


def getting_started_candlesticks(request):
    return render(request, 'getting_started_candlesticks.html')


def single_cad_patterns_part1(request):
    return render(request, 'single_cad_patterns_part1.html')


def single_cad_patterns_part2(request):
    return render(request, 'single_cad_patterns_part2.html')


def single_cad_patterns_part3(request):
    return render(request, 'single_cad_patterns_part3.html')


def support_resistance(request):
    return render(request, 'support_resistance.html')


def volumes(request):
    return render(request, 'volumes.html')


def moving_averages(request):
    return render(request, 'moving_averages.html')


def indicators(request):
    return render(request, 'indicators.html')


def dow_theory_1(request):
    return render(request, 'dow_theory_1.html')


def dow_theory2(request):
    return render(request, 'dow_theory2.html')


def news(request):
    api_request = requests.get(
        "https://api.polygon.io/v2/reference/news?limit=10&order=descending&sort=published_utc&ticker=AAPL&published_utc.gte=2021-04-26&apiKey=XL5JZiyXF4aVL6zzsnVpp8jg4gYXp9ta")
    api = json.loads(api_request.content)
    return render(request, 'news.html', {'api': api, })


def handelSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) > 25:
            messages.error(
                request, " Your user name must be under 25 characters")
            return redirect('index')
          
        if not username.isalnum():
            messages.error(
                request, " User name should only contain letters and numbers")
            return redirect('index')
        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('index')
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        level = Level()
        level.uname = username
        level.save()
        bal = Balance()
        bal.uname = username
        bal.save()
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(
            request, " Your Account has been successfully created")
        return redirect('index')
    else:
        return HttpResponse('404 - NOT FOUND')


def handelLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("index")

    return HttpResponse("404- Not found")

    return HttpResponse("login")


def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('index')
    return HttpResponse('handelLogout')


def sell(request, stockname):
    from .models import Balance
    from .models import Portfolio
    usname = request.user
    name = usname.username
    balance = Balance.objects.get(uname=name)
    data = Portfolio.objects.filter(uname=name, ticker=stockname)
    # op = []
    tickerss = []
    cp = []
    for q in data:
        t = q.ticker
        tickerss.append(t)

    for item in tickerss:
        data_nse = nse_eq(item)
        lastPrice = data_nse["priceInfo"]["lastPrice"]
        cp.append(lastPrice)

    # for item in data:
    #     api_request = nsepy.get_quote(item)
    #     api_request.pop("tradedDate")
    #     a = api_request.get("data")
    #     ab = a[0]

    #     try:
    #         op.append(ab)
    #     except Exception as e:
    #         api_request = "Error..."

    context = {
        'data': data,
        'cp': cp
    }
    return render(request, 'sell.html', context)


def finalSell(request):
    if request.method == "POST":
        sname = request.POST["sname"]
        sprice = request.POST["sprice"]
        quan = request.POST["quan"]
        lprice = request.POST["lprice"]
    context = {
        'quan': quan,
        'sname': sname,
        'sprice': sprice,
        'lprice': lprice,
    }
    return render(request, 'finalSell.html', context)


def transactions(request):
    from .models import Balance
    from .models import Portfolio
    from .models import Sell
    # import nsepy
    usname = request.user
    name = usname.username
    import time
    ym = time.strftime("%Y-%m")
    if request.method == "POST":
        sname = request.POST["sname"]
        sprice = request.POST["sprice"]
        quan = request.POST["quan"]
        lprice = request.POST["lprice"]
        sell = Sell()
        sell.uname = name
        sell.ticker = sname
        sell.buyPrice = sprice
        sell.quantity = quan
        sell.sellPrice = lprice
        sell.month = ym
        sell.save()
        bal = Balance.objects.get(uname=name)
        bal.balance = bal.balance + (float(lprice)*float(quan))
        bal.save(update_fields=['balance'])
        data = Portfolio.objects.get(uname=name, ticker=sname)
        if data.quantity > int(quan):
            data.quantity = data.quantity - int(quan)
            data.save(update_fields=['quantity'])
        elif data.quantity == int(quan):
            data.delete()

        return redirect(transactions)
    else:

        data = Sell.objects.filter(uname=name)
        level = Level.objects.get(uname=name)
        profit = []
        for q in data:
            profit1 = (q.sellPrice*q.quantity) - (q.buyPrice*q.quantity)
            profit1 = round(profit1, 2)
            profit.append(float(profit1))
        total = sum(profit)
        total = round(total, 2)
        if total > 100:
            level.level = 1
            level.save(update_fields=['level'])
        if total > 500:
            level.level = 2
            level.save(update_fields=['level'])
        if total > 1000:
            level.level = 3
            level.save(update_fields=['level'])
        # ticker = data.ticker
        # data_nse = nsepy.get_quote(ticker)
        # lastPrice = data_nse["data"][0]["lastPrice"]
        # op = []
        # for item in data:
        #     api_request = nsepy.get_quote(item)
        #     api_request.pop("tradedDate")
        #     a = api_request.get("data")
        #     ab = a[0]

        #     try:
        #         op.append(ab)
        #     except Exception as e:
        #         api_request = "Error..."
        data1 = Transaction.objects.filter(uname=name)
        # # ticker = data.ticker
        # # data_nse = nsepy.get_quote(ticker)
        # # lastPrice = data_nse["data"][0]["lastPrice"]
        # op1 = []
        # for item in data1:
        #     api_request = nsepy.get_quote(item)
        #     api_request.pop("tradedDate")
        #     a = api_request.get("data")
        #     ab = a[0]

        #     try:
        #         op1.append(ab)
        #     except Exception as e:
        #         api_request = "Error..."

    context = {
        # 'op': op,
        'data': data,
        # 'op1': op1,
        'data1': data1,
        'profit': profit,
        'total': total,
        'level': level,
    }
    return render(request, 'transactions.html', context)


def BuyPage(request):
    from pytz import timezone
    from datetime import datetime
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S')
    market_open = "09:15:00"
    market_close = "15:30:00"
    # MARKET TIME
    import calendar
    from datetime import date
    curr_date = date.today()
    day = calendar.day_name[curr_date.weekday()]
    if ((market_open <= ind_time <= market_close) and ((day != "Saturday") and (day != "Sunday"))):
        isopen = 1
    else:
        isopen = 0
    context = {
        'isopen': isopen,
    }
    return render(request, 'buypage.html', context)

# change


def SellPage(request):
    # import nsepy
    from nsepython import nse_eq
    usname = request.user
    name = usname.username
    data = Portfolio.objects.filter(uname=name)
    profit = []
    bp = []
    cp = []
    quan = []
    bpintoquan = []
    cpintoquan = []
    percent = []
    tickerss = []
    invested = 0

    for q in data:
        l = q.quantity
        t = q.ticker
        tickerss.append(t)
        quan.append(int(l))

    for i in data:
        a = i.buyPrice
        bp.append(float(a))

    for k in range(len(bp)):
        b = bp[k]*quan[k]
        bpintoquan.append(b)

    for item in tickerss:
        data_nse = nse_eq(item)
        lastPrice = data_nse["priceInfo"]["lastPrice"]
        cp.append(lastPrice)

    for k in range(len(cp)):
        b = cp[k]*quan[k]
        cpintoquan.append(b)

    for j in range(len(cp)):
        profit.append(cpintoquan[j]-bpintoquan[j])

    for l in range(len(profit)):
        p = (profit[l]*100)/cpintoquan[l]
        p = round(p, 2)
        percent.append(p)
    invested = sum(bpintoquan)
    current = sum(cpintoquan)
    totalreturn = current - invested
    if invested == 0:
        returnpercent = (totalreturn/1)*100
    else:
        returnpercent = (totalreturn/invested)*100
    returnpercent = round(returnpercent, 2)
    context = {
        'data': data,
        'bpintoquan': bpintoquan,
        'invested': invested,
    }
    return render(request, 'sellpage.html', context)



def portfolio(request):
    # import nsepy
    from nsepython import nse_eq
    usname = request.user
    name = usname.username
    balance = Balance.objects.get(uname=name)
    data = Portfolio.objects.filter(uname=name)
    selldata = Sell.objects.filter(uname=name)

    companyname = []
    quantity = []
    investedvalue = []
    marketprice = []
    currentvalue = []
    profit = []
    percent = []
    sector = []

    for s in data:
        data_nse = nse_eq(s.ticker)
        sector.append(data_nse['industryInfo']['sector'])

    for c in data:
        l = c.ticker
        companyname.append(l)

    for q in data:
        l = q.quantity
        quantity.append(int(l))

    for i in data:
        l = i.quantity * i.buyPrice
        investedvalue.append(l)

    for item in companyname:
        data_nse2 = nse_eq(item)
        x = data_nse2["priceInfo"]["lastPrice"]
        marketprice.append(x)

    currentvalue = [quantity[i] * marketprice[i] for i in range(len(quantity))]

    for j in range(len(quantity)):
        profit.append(currentvalue[j]-investedvalue[j])

    for l in range(len(profit)):
        p = (profit[l]*100)/currentvalue[l]
        p = round(p, 2)
        percent.append(p)

    # bargraph
    janinv = []
    febinv = []
    marinv = []
    aprinv = []
    mayinv = []
    juninv = []
    julinv = []
    auginv = []
    sepinv = []
    octinv = []
    novinv = []
    decinv = []

    jandata = Portfolio.objects.filter(uname=name, month="2023-01")
    for i in jandata:
        l = i.quantity * i.buyPrice
        janinv.append(l)

    febdata = Portfolio.objects.filter(uname=name, month="2023-02")
    for i in febdata:
        l = i.quantity * i.buyPrice
        febinv.append(l)

    mardata = Portfolio.objects.filter(uname=name, month="2023-03")
    for i in mardata:
        l = i.quantity * i.buyPrice
        marinv.append(l)

    aprdata = Portfolio.objects.filter(uname=name, month="2023-04")
    for i in aprdata:
        l = i.quantity * i.buyPrice
        aprinv.append(l)

    maydata = Portfolio.objects.filter(uname=name, month="2023-05")
    for i in maydata:
        l = i.quantity * i.buyPrice
        mayinv.append(l)

    jundata = Portfolio.objects.filter(uname=name, month="2023-06")
    for i in jundata:
        l = i.quantity * i.buyPrice
        juninv.append(l)

    bardata = [sum(janinv), sum(febinv), sum(marinv),
               sum(aprinv), sum(mayinv), sum(juninv)]

    buytotal = []
    selltotal = []
    for i in selldata:
        l = i.quantity * i.buyPrice
        buytotal.append(l)

    for i in selldata:
        l = i.quantity * i.sellPrice
        selltotal.append(l)

    context = {
        'companyname': companyname,
        'quantity': quantity,
        'investedvalue': investedvalue,
        'marketprice': marketprice,
        'currentvalue': currentvalue,
        'profit': profit,
        'percent': percent,
        'data': data,
        'sector': sector,
        'bardata': bardata,
        'selldata': selldata,
        'buytotal': buytotal,
        'selltotal': selltotal,
    }

    return render(request, 'portfolio.html', context)


def buy(request):
    usname = request.user
    name = usname.username
    balance = Balance.objects.get(uname=name)
    from nsepython import nse_eq

    if request.method == "POST":
        ticker = request.POST["ticker"]
        data_nse = nse_eq(ticker)
        companyName = data_nse['info']['companyName']
        lastPrice = data_nse["priceInfo"]["lastPrice"]
        dayHigh = data_nse["priceInfo"]["intraDayHighLow"]["max"]
        dayLow = data_nse["priceInfo"]["intraDayHighLow"]["min"]
        
        high52 = data_nse["priceInfo"]["weekHighLow"]["max"]
        low52 = data_nse["priceInfo"]["weekHighLow"]["min"]
        
        previousClose = data_nse["priceInfo"]["previousClose"]
        open = data_nse["priceInfo"]["open"]
        pChange = data_nse["priceInfo"]["pChange"]
        change = data_nse["priceInfo"]["change"]
        totalTradedVolume = data_nse["preOpenMarket"]["totalTradedVolume"]

    context = {
        'balance': balance,
        'ticker': ticker,
        'companyName': companyName,
        'lastPrice': lastPrice,
        'dayHigh': dayHigh,
        'dayLow': dayLow,
        'high52': high52,
        'low52': low52,
        'previousClose': previousClose,
        'open': open,
        'pChange': pChange,
        'change': change,
        'totalTradedVolume': totalTradedVolume,
        # 'data1': data1,
        # 'count1': count1
    }
    return render(request, 'buy.html', context)


def finalBuy(request):
    import math
    usname = request.user
    name = usname.username
    balance = Balance.objects.get(uname=name)
    if request.method == "POST":
        quan = request.POST["quan"]
        sname = request.POST["sname"]
        sprice = request.POST["sprice"]
        sprice = sprice.replace(",", "")
        ticker = request.POST["ticker"]
        total = float(sprice)*float(quan)
    balance1 = balance.balance
    buyQuan = math.floor(balance1/float(sprice))
    context = {
        'balance': balance,
        'balance1': balance1,
        'quan': quan,
        'sname': sname,
        'sprice': sprice,
        'ticker': ticker,
        'total': total,
        'buyQuan': buyQuan,
    }
    return render(request, 'finalbuy.html', context)

def trade(request):
    from django.core.mail import send_mail
    from .models import Balance
    from .models import Portfolio
    from .models import Transaction
    from nsepython import nse_eq
    usname = request.user
    name = usname.username
    email = usname.email
    balance = Balance.objects.get(uname=name)
    from pytz import timezone
    from datetime import datetime
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S')
    market_open = "09:15:00"
    market_close = "15:30:00"
    import time
    ym = time.strftime("%Y-%m")
    if request.method == "POST":
        sname = request.POST["sname"]
        sprice = request.POST["sprice"]
        quan = request.POST["quan"]
        ticker = request.POST["ticker"]
        if Portfolio.objects.filter(uname=name, ticker=ticker).exists():
            data1 = Portfolio.objects.get(uname=name, ticker=ticker)
            tq = data1.quantity + int(quan)
            data1.quantity = data1.quantity + int(quan)
            data1.buyPrice = (data1.buyPrice+float(sprice))/2
            data1.month = ym
            data1.save(update_fields=['quantity', 'buyPrice'])
            bal1 = Balance.objects.get(uname=name)
            bal1.balance = bal1.balance - (float(sprice)*float(quan))
            bal1.save(update_fields=['balance'])
            tran = Transaction()
            tran.uname = name
            tran.ticker = ticker
            tran.buyPrice = sprice
            tran.quantity = quan
            tran.month = ym
            tran.save()
            # send_mail(
            #     "Buy Transaction",
            #     "Hello!! "+name+"\nyou have Buyed "+ticker +
            #     " with "+quan+" quantity at price " +
            #     sprice+"\nTotal Quantity: "+str(tq),
            #     'mohonab16@gmail.com',
            #     [email],
            #     fail_silently=False,
            # )
            return redirect('index')
        else:
            port = Portfolio()
            port.uname = name
            port.ticker = ticker
            port.buyPrice = sprice
            port.quantity = quan
            port.month = ym
            port.save()
            tran = Transaction()
            tran.uname = name
            tran.ticker = ticker
            tran.buyPrice = sprice
            tran.quantity = quan
            tran.month = ym
            tran.save()
            bal = Balance.objects.get(uname=name)
            bal.balance = bal.balance - (float(sprice)*float(quan))
            bal.save(update_fields=['balance'])

            return redirect('portfolio')

    else:

        data = Portfolio.objects.filter(uname=name)
        data1 = Portfolio.objects.all()
        count = len(data)
        profit = []
        bp = []
        cp = []
        quan = []
        bpintoquan = []
        cpintoquan = []
        percent = []

        for q in data:
            l = q.quantity
            quan.append(int(l))

        for i in data:
            a = i.buyPrice
            bp.append(float(a))

        for k in range(len(bp)):
            b = bp[k]*quan[k]
            bpintoquan.append(b)

        for item in data:
            api_request = nse_eq(item)
            api_request.pop("tradedDate")
            a = api_request.get("data")
            h = a["priceInfo"]["lastPrice"]

            try:
                cp.append(float(h))
            except Exception as e:
                api_request = "Error..."

        for k in range(len(cp)):
            b = cp[k]*quan[k]
            cpintoquan.append(b)

        for j in range(len(cp)):
            profit.append(cpintoquan[j]-bpintoquan[j])

        for l in range(len(profit)):
            p = (profit[l]*100)/cpintoquan[l]
            p = round(p, 2)
            percent.append(p)

        invested = sum(bpintoquan)
        current = sum(cpintoquan)
        totalreturn = current - invested
        if invested == 0:
            returnpercent = (totalreturn/1)*100
        else:
            returnpercent = (totalreturn/invested)*100
        returnpercent = round(returnpercent, 2)
    # RECETN TRANSACTION
    from datetime import date
    today = date.today()
    data12 = Portfolio.objects.filter(buyDate=today)
    # MARKET TIME
    import calendar
    curr_date = date.today()
    day = calendar.day_name[curr_date.weekday()]
    if ((market_open <= ind_time <= market_close) and ((day != "Saturday") and (day != "Sunday"))):
        isopen = 1
    else:
        isopen = 0
    context = {
        'balance': balance,
        'cp': cp,
        'bpintoquan': bpintoquan,
        'cpintoquan': cpintoquan,
        'profit': profit,
        'count': count,
        # 'count1': count1,
        'percent': percent,
        'invested': invested,
        'current': current,
        'totalreturn': totalreturn,
        'returnpercent': returnpercent,
        'data': data,
        'data1': data1,
        'email': email,
        'data12': data12,
        'isopen': isopen,
    }
    return render(request, 'portfolio.html', context)


def csv_month(request):
    import csv
    import time
    ym = time.strftime("%Y-%m")
    from datetime import date
    today = date.today()
    usname = request.user
    name = usname.username
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=EasyTrade.csv'
    writer = csv.writer(response)
    data = Transaction.objects.filter(uname=name, month=ym)
    writer.writerow(['Ticker', 'Buy Price', 'Quantity', 'Buy Date'])
    for i in data:
        writer.writerow([i.ticker, i.buyPrice, i.quantity, i.buyDate])
    return response