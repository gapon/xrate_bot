from xml.sax.handler import DTDHandler
import tinvest
from tinvest import schemas
from datetime import datetime, date, timedelta
from pytz import timezone
import os

TOKEN = os.getenv('TI_SANDBOX_TOKEN')

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
    #return r.payload.candles

#current_time = datetime.now(timezone('UTC'))
#rint(ticker_price_on_date(USD_TICKER, current_time))

