import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf 
import math
import sqlite3 
import time

from config import db_name, interval ,view_limit,row_limit,TICKER
def get_connection():
    return sqlite3.connect(db_name)
def init_db():
    conn=sqlite3.connect(db_name)
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
    LIMIT MAX(0,(SELECT COUNT(*) FROM stock_prices)-{row_limit})
    );
    END;
    ''')
    conn.commit()
    conn.close()


          


