import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import datetime as dt

ticker = companyName
start = dt.datetime(2019, 1, 1)
end = dt.datetime(2020, 12, 31)
data = yf.download(tickers=companyName, period='365d', interval='1h')
data["date"] = data.index


data.reset_index()
data['MA20'] = data['Close'].rolling(20).mean().tolist()
data['EMA20'] = data['Close'].ewm(span=10, adjust=False).mean()
movingAverages = data['MA20'].tolist()
exponentialMovingAverages= data['EMA20'].tolist()
MA = []
EMA = []
for i in movingAverages:
    MA.append(float(f'{float(f"{i:.4g}"):g}'))
for i in exponentialMovingAverages:
    EMA.append(float(f'{float(f"{i:.4g}"):g}'))



intersectPrices = []
data['Intersect'] = "NaN"
## Buying Points
for i in range(1,len(data)):
    if (data.iloc[i]['EMA20'] < data.iloc[i]['MA20']) and (data.iloc[i-1]['EMA20'] > data.iloc[i-1]['MA20']):# and (data.iloc[i]['EMA20'] - data.iloc[i-1]['EMA20']) >= 0):
        dateLocation = data.iloc[i]['date']
        data.loc[dateLocation,"Intersect"] = "Buy"
    
    
##CLOSING INTERCEPTS
for i in range(1,len(data)):
    if (data.iloc[i]['EMA20'] > data.iloc[i]['MA20']) and (data.iloc[i-1]['EMA20'] < data.iloc[i-1]['MA20']):
        intersectPrices.append(data.iloc[i]['Open'])
        dateLocation = data.iloc[i]['date']
        data.loc[dateLocation,"Intersect"] = "Sell"

sumGain = 0
BuyPrice = 0
Holding = False
for i in range(1,len(data),1):
    if(data.iloc[i]['Intersect'] == "Buy"):
        BuyPrice = data.iloc[i]['Open']
        Holding = True
    if((data.iloc[i]['Intersect'] == "Sell") and Holding):
        sumGain = sumGain + (BuyPrice - data.iloc[i]['Close'])
        Holding = False
if sumGain <= 0:
    print("-$" + str(abs(sumGain)) + " " + comp)
else:
    print("$" + str(sumGain) + " " + comp)
