import pandas as pd 
import numpy as np
import math
import yfinance as yf 
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
import  time ,sqlite3
from config import db_name,interval,TICKER
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
            return sma
        except Exception as e:
            print(f"error:{e}")
        time.sleep(interval)

def bollinger_up_down(db_name,table_name):
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
            return latest_ema
            
        except Exception as e:
            print(f"error:{e}")
        time.sleep(interval)



def rsi(db_name,table_name):
    while True :
        try:
            query=f"SELECT Close FROM {table_name} ORDER BY rowid DESC LIMIT 14"
            conn=sqlite3.connect(db_name)
            df=pd.read_sql(query,conn)
            conn.close()
            if df.empty or len(df)<14:
                print("insufficient data")
            delta=df["Close"].diff()
            gains=delta.where(delta>0,0.0)
            loss=-delta.where(delta<0,0.0)
            avg_gain=gains.mean()
            avg_loss=loss.mean()
            rs=avg_gain/avg_loss
            rsi_value=100-(100/(1+rs))
            return rsi_value
        except Exception as e:
            print(f"error:{e}")
        time.sleep(interval)

            



        
def store_factors(db_name,table_name):
    while True:
        try:
            latest_sma_20=sma_20(db_name,table_name)
            latest_ema_20=ema_20(db_name,table_name)
            bollinger_up,bollinger_down=bollinger_up_down(db_name,table_name)
            volat=volatiliy(db_name,table_name)
            conn=sqlite3.connect(db_name)
            cursor=conn.cursor()
            cursor.execute('''INSERT OR IGNORE INTO indicators (ticker,volatility,sma_20,ema_20,rsi,bollinger_upper,bollinger_down) VALUES(?,?,?,?,?,?,?)''',(TICKER,volat,latest_sma_20,latest_ema_20,rsi(db_name,table_name),bollinger_up,bollinger_down))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"exceprion:{e}")
        time.sleep(interval)


        



        
