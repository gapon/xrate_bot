from datetime import datetime, date, timedelta
from pytz import timezone
import os
import requests
from tinkoff.invest.sandbox.client import SandboxClient
from tinkoff.invest import CandleInterval, Quotation
from tinkoff.invest.utils import now, quotation_to_decimal
from tinkoff.invest.exceptions import RequestError
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns



TOKEN = os.getenv('TI_SANDBOX_TOKEN')
BINANCE_API = 'https://api.coindesk.com/v1/bpi/currentprice.json'
figi_cny = 'BBG0013HRTL0'
figi_usd = 'BBG0013HGFT4'
figi_tmos = 'BBG333333333'
figi_dict = {'CNY':'BBG0013HRTL0', 'TMOS':'BBG333333333', 'USD':'BBG0013HGFT4'}

def get_figi_price(figi: str) -> float:
    try:
        with SandboxClient(TOKEN) as client:
            candles = list(client.get_all_candles(
                figi=figi,
                from_=now() - timedelta(minutes=1),
                interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
            ))
        
        return round(quotation_to_decimal(candles[-1].close), 3)
    except:
        return 'NA'

def get_btc_rate():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    return data['bpi']['USD']['rate']

def get_all_figi_prices() -> str:
    text = ""
    for figi in figi_dict:
        figi_price = get_figi_price(figi_dict[figi])
        text = text + f"{figi}: {figi_price} \n"
    return text

def get_candles_for_period(figi: str, period: int):
    with SandboxClient(TOKEN) as client:
        candles = list(client.get_all_candles(
                figi=figi,
                from_=now() - timedelta(days=period),
                interval=CandleInterval.CANDLE_INTERVAL_DAY,
            ))
        return candles

def create_candles_df(candles):
    df = pd.DataFrame(candles)
    df['close'] = df['close'].apply(lambda x: quotation_to_decimal(Quotation(x['units'], x['nano'])))   
    df['date'] = df['time'].dt.date
    return df

def plot_candles(df):
    plt.figure(figsize=(15,10))
    ax = sns.lineplot(df, x=df['date'], y=df['close'])
    plt.savefig('output.png')