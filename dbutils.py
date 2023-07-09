import sqlite3
from contextlib import closing

DB_NAME = 'xrate.sqlite'

def create_tickers_table(tickers_df):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        tickers_df.to_sql('tickers', conn, if_exists='replace', index=False)
    return 0

def get_figi_by_ticker(ticker: str) -> str:
    ticker = ticker.upper()
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with closing(conn.cursor()) as cur:
            sql = 'SELECT figi FROM tickers WHERE ticker = (?)'
            args = (ticker, )
            figi = cur.execute(sql, args).fetchall()
    return figi[0][0]