import pandas as pd 
import numpy as np
import math
import yfinance as yf 
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
import  time ,sqlite3
from config import db_name,interval
def volatiliy(db_name,table_name):
    while True:
        try:
            query=f"SELECT Close FROM {table_name} ORDER BY rowid DESC LIMIT 60"
            conn=sqlite3.connect(db_name)
            df=pd.read_sql(query,conn)
            volat=df.std()
            
                
        except Exception as e:
            print(f"error:{e}")
        time.sleep(interval)

def sma_20(db_name ,table_name):
    while True:
        try:
            query=f'SELECT CLOSE FROM {table_name} ORDER BY rowid DESC LIMIT 20'
            conn=sqlite3.connect(db_name)
            df=pd.read_sql(query,conn)
            sma=df.mean()
        except Exception as e:
            print(f"error:{e}")
        time.sleep(interval)

def bollinger_u_downp(db_name,table_name):
    while True:
        try:
            avg=sma_20(db_name,table_name)
            gap=volatiliy(db_name,table_name)
            bollinger_up=avg+2*gap
            bollinger_down=avg-2*volatiliy
            return bollinger_up,bollinger_down
        except Exception as e:
            print(f"error:{e}")
        time.sleep(interval)

def ema_20(db_name,table_name):
    while True:
        try:
            multiplier=2/21
            query=f"SELECT CLOSE FROM {table_name} ORDER BY rowid DESC LIMIT 20"
            conn=sqlite3.connect(db_name)
            df=pd.read_sql(query,conn)
            conn.close()
            if df.empty or len(df)<20:
                print("insufficient data ")
            df=df.iloc[:-1].reset_index(drop=True)
            df['ema_20']=df['CLOSE'].ewm(span=20,adjust=False).mean()
            latest_ema=df['ema_20'].iloc[-1]
            print(latest_ema)
            
        except Exception as e:
            print(f"error:{e}")
        time.sleep(interval)
        



        
