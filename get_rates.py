from xml.sax.handler import DTDHandler
import tinvest
from tinvest import schemas
from datetime import datetime, date, timedelta
from pytz import timezone
import os
import requests


TOKEN = os.getenv('TI_SANDBOX_TOKEN')
BINANCE_API = 'https://api.coindesk.com/v1/bpi/currentprice.json'
USD_TICKER = 'USD000UTSTOM'

client = tinvest.SyncClient(TOKEN, use_sandbox=True)

def get_figi_by_ticker(ticker : str):
    r = client.get_market_search_by_ticker(ticker)
    return r.payload.instruments[0].figi

def ticker_price_on_date(ticker : str, dt : datetime):
    start_dttm = dt - timedelta(minutes = 5)
    end_dttm = dt
    figi = get_figi_by_ticker(ticker)
    r = client.get_market_candles(figi=figi, from_=start_dttm, to=end_dttm, interval=schemas.CandleResolution.min1)
    return float(r.payload.candles[-1].c)

def get_usd_rate():
    current_time = datetime.now(timezone('UTC'))
    try:
        usd_rate = ticker_price_on_date(USD_TICKER, current_time)
        return usd_rate
    except IndexError:
        print('No Candles Data')

    

def get_btc_rate():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    return data['bpi']['USD']['rate']

