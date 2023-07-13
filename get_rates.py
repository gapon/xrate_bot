from datetime import datetime, date, timedelta
from pytz import timezone
import os
import requests
from tinkoff.invest.sandbox.client import SandboxClient
from tinkoff.invest import CandleInterval, Quotation
from tinkoff.invest.utils import now, quotation_to_decimal
from tinkoff.invest.exceptions import RequestError
import pandas as pd
from tinkoff.invest.services import InstrumentsService
from dbutils import get_figi_by_ticker

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

TOKEN = os.getenv('TI_SANDBOX_TOKEN')
BINANCE_API = 'https://api.coindesk.com/v1/bpi/currentprice.json'
currency_dict = {'CNY':'BBG0013HRTL0', 'USD':'BBG0013HGFT4'}

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
    for figi in currency_dict:
        figi_price = get_figi_price(currency_dict[figi])
        text = text + f"{figi}: {figi_price} \n"
    return text

def get_candles_for_period(figi: str, period: int):
    with SandboxClient(TOKEN) as client:
        candles = list(client.get_all_candles(
                figi=figi,
                from_=now() - timedelta(days=period),
                interval=CandleInterval.CANDLE_INTERVAL_DAY,
            ))
        candles_df = pd.DataFrame(candles)
        candles_df['close price'] = candles_df['close'].apply(lambda x:quotation_to_decimal(Quotation(x['units'], x['nano'])))
        candles_df['date'] = candles_df['time'].dt.date
        df_cols = ['date', 'close price']
        return candles_df[df_cols]

def plot_candles(df, ticker):

    plt.figure(figsize=(15,10))
    ax = sns.lineplot(df, x=df['date'], y=df['close price'], label='close price')
    
    if len(df) > 50:
        df['MA50'] = df['close price'].rolling(window=50).mean()
        sns.lineplot(df, x=df['date'], y=df['MA50'], label='MA50')
    
    if len(df) > 200:
        df['MA200'] = df['close price'].rolling(window=200).mean()
        sns.lineplot(df, x=df['date'], y=df['MA200'], label='MA200')

    plt.grid()
    plt.title(ticker.upper(), fontsize = 25)
    plt.legend()
    plt.savefig('output.png')
    
def get_tickers_df():
    with SandboxClient(TOKEN) as client:
        instruments: InstrumentsService = client.instruments
        tickers = []
        for method in ['shares', 'etfs']:
            for item in getattr(instruments, method)().instruments:
                tickers.append(
                    {
                        'ticker': item.ticker,
                        'figi': item.figi,
                    }
                )    
    tickers_df = pd.DataFrame(tickers)
    currency_df = pd.DataFrame(currency_dict.items(), columns = ['ticker', 'figi'])
    tickers_df = pd.concat([tickers_df, currency_df], ignore_index=True)

    return tickers_df

    
def chart_ticker_for_period(ticker: str, period: int) -> None:
    figi = get_figi_by_ticker(ticker)
    candles_df = get_candles_for_period(figi, period)
    plot_candles(candles_df, ticker)