from datetime import datetime, date, timedelta
from pytz import timezone
import os
import requests
from tinkoff.invest.sandbox.client import SandboxClient
from tinkoff.invest import CandleInterval
from tinkoff.invest.utils import now, quotation_to_decimal


TOKEN = os.getenv('TI_SANDBOX_TOKEN')
BINANCE_API = 'https://api.coindesk.com/v1/bpi/currentprice.json'
figi_cny = 'BBG0013HRTL0'
figi_usd = 'BBG0013HGFT4'
figi_tmos = 'BBG333333333'
figi_dict = {'CNY':'BBG0013HRTL0', 'TMOS':'BBG333333333', 'USD':'BBG0013HGFT4'}

def get_figi_price(figi: str) -> float:
    with SandboxClient(TOKEN) as client:
        candles = list(client.get_all_candles(
            figi=figi,
            from_=now() - timedelta(minutes=1),
            interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
        ))
    try:
        return quotation_to_decimal(candles[-1].close)
    except IndexError:
        return 'No Candle'

def get_btc_rate():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    return data['bpi']['USD']['rate']

def get_all_figi_prices() -> str:
    text = ""
    for figi in figi_dict:
        figi_price = get_figi_price(figi_dict[figi])
        text = text + f"{figi}: {figi_price:.3f} \n"
    return text

