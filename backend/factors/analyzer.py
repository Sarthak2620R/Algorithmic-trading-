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
        

