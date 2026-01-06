import yfinance as yf                     
import pandas as pd                     
import numpy as np                        
import matplotlib.pyplot as plt           
import plotly.graph_objects as go         

data = yf.download("INFY.NS", start="2020-01-01", end="2025-01-01")

print(data.head())

#Calculate Moving Averages
data['20_MA'] = data['Close'].rolling(window=20).mean()   
data['50_MA'] = data['Close'].rolling(window=50).mean()   

#Generate buy, sell signal
data['Signal'] = 0
data['Signal'][20:] = np.where(data['20_MA'][20:] > data['50_MA'][20:], 1, 0)  #Buy if 20_MA > 50_MA
data['Position'] = data['Signal'].diff()   

print(data.tail())

plt.figure(figsize=(12,6))
plt.plot(data['Close'], label='INFY Close', alpha=0.6)
plt.plot(data['20_MA'], label='20-day MA', alpha=0.9)
plt.plot(data['50_MA'], label='50-day MA', alpha=0.9)


plt.plot(data[data['Position'] == 1].index,
         data['20_MA'][data['Position'] == 1],
         '^', markersize=12, color='g', label='Buy Signal')

plt.plot(data[data['Position'] == -1].index,
         data['20_MA'][data['Position'] == -1],
         'v', markersize=12, color='r', label='Sell Signal')

plt.title("Infosys Stock Trend with 20 & 50 Day Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (INR)")
plt.legend()
plt.grid(True)
plt.show()


data['Daily_Return'] = data['Close'].pct_change()  
data['Strategy_Return'] = data['Daily_Return'] * data['Signal'].shift(1)  


cumulative_strategy = (1 + data['Strategy_Return']).cumprod()
cumulative_stock = (1 + data['Daily_Return']).cumprod()

volatility = data['Daily_Return'].std() * np.sqrt(252)
print("Annualized Volatility of INFY:", round(volatility, 4))

#Compare 
plt.figure(figsize=(12,6))
plt.plot(cumulative_stock, label="Buy & Hold INFY", color="blue")
plt.plot(cumulative_strategy, label="MA Crossover Strategy", color="orange")
plt.title("Strategy vs Stock Returns")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.grid(True)
plt.show()

#dashboard
fig = go.Figure()

fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close Price'))
fig.add_trace(go.Scatter(x=data.index, y=data['20_MA'], name='20-day MA'))
fig.add_trace(go.Scatter(x=data.index, y=data['50_MA'], name='50-day MA'))

fig.update_layout(title="Infosys Stock Interactive Dashboard",
                  xaxis_title="Date",
                  yaxis_title="Price (INR)",
                  template="plotly_dark",
                  legend=dict(x=0, y=1))

fig.show()
