import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf 
import math
import sqlite3 
import time
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from configparser import db_name, interval ,view_limit,row_limit
TICKER='APPL'
db_name="stock_data.db"
interval=60
row_limt=10000
def get_connection():
    return sqlite3.connect(db_name)
def init_db():
    conn=sqlite3.connect("stock_data.db")
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS stock_prices
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    ticker TEXT ,
    open REAL ,
    high REAL,
    low REAL,
    closed REAL,
    volume REAL
    )
    """)
    cursor.execute(f'''
    CREATE TRIGGER IF NOT EXISTS cap_table_size
    AFTER INSERT ON stock_prices
    BEGIN
    DELETE FROM stock_prices
    WHERE id IN (
    SELECT id FROM stock_prices
    ORDER BY timestamp ASC, id ASC
    LIMIT MAX(0,(SELECT COUNT(*) FROM stock_prices)-{row_limt}
    );
    END;
    ''')
    conn.commit()
    conn.close()

def data_logger_thread():
    print(f"background thread started logging {TICKER} date...")
    ticker_obj=yf.Ticker(TICKER)
    while True:
        try:
            df=ticker_obj.hsitory(period="1d",interval="1m")
            if not df.empty:
                latest_time=df.index[-1].strftime('%Y,%m,%d %H:%M:%S')
                row=df.iloc[-1]
                open=row['open']
                high=row['high']
                low=row['low']
                close=row['close']
                volume=int(row['volume'])
                conn=sqlite3.connect(db_name)
                cursor=conn.cursor()
                cursor.execute('''INSERT OR IGNORE INTO stock_prices(timestamp,ticker ,open,high,low,close,volume) VALUES(?,?,?,?,?,?,?)''',(latest_time,TICKER,open,high,low,close,volume))
                conn.commit()
                conn.close()
        except Exception as e:
            print(f"fetch error:{e}")
        time.sleep(interval)

          


