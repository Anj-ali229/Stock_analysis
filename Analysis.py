# STEP 1: Install required libraries (run this in a Jupyter Notebook or terminal)
# !pip install yfinance plotly seaborn

#  STEP 2: Import necessary libraries
import yfinance as yf                     # For downloading stock data
import pandas as pd                       # For data manipulation
import numpy as np                        # For numerical operations
import matplotlib.pyplot as plt           # For static visualizations
import plotly.graph_objects as go         # For interactive visualizations

#  STEP 3: Download Infosys stock data from Yahoo Finance (NSE ticker: INFY.NS)
data = yf.download("INFY.NS", start="2020-01-01", end="2025-01-01")

#  Preview first few rows of the dataset
print(data.head())

#  STEP 4: Calculate Moving Averages
data['20_MA'] = data['Close'].rolling(window=20).mean()   # 20-day moving average
data['50_MA'] = data['Close'].rolling(window=50).mean()   # 50-day moving average

#  STEP 5: Generate Buy/Sell Signals based on MA crossover
data['Signal'] = 0
data['Signal'][20:] = np.where(data['20_MA'][20:] > data['50_MA'][20:], 1, 0)  # Buy if 20_MA > 50_MA
data['Position'] = data['Signal'].diff()   # 1 = Buy signal, -1 = Sell signal

#  View last few rows to inspect signals
print(data.tail())

# 🖼 STEP 6: Visualize Stock Price with Moving Averages and Buy/Sell Signals
plt.figure(figsize=(12,6))
plt.plot(data['Close'], label='INFY Close', alpha=0.6)
plt.plot(data['20_MA'], label='20-day MA', alpha=0.9)
plt.plot(data['50_MA'], label='50-day MA', alpha=0.9)

# Mark Buy signals with green upward arrows
plt.plot(data[data['Position'] == 1].index,
         data['20_MA'][data['Position'] == 1],
         '^', markersize=12, color='g', label='Buy Signal')

# Mark Sell signals with red downward arrows
plt.plot(data[data['Position'] == -1].index,
         data['20_MA'][data['Position'] == -1],
         'v', markersize=12, color='r', label='Sell Signal')

plt.title("Infosys Stock Trend with 20 & 50 Day Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (INR)")
plt.legend()
plt.grid(True)
plt.show()

#  STEP 7: Calculate Returns and Annualized Volatility
data['Daily_Return'] = data['Close'].pct_change()  # Daily percentage change
data['Strategy_Return'] = data['Daily_Return'] * data['Signal'].shift(1)  # Strategy returns based on signals

# Cumulative returns over time
cumulative_strategy = (1 + data['Strategy_Return']).cumprod()
cumulative_stock = (1 + data['Daily_Return']).cumprod()

# Annualized volatility (standard deviation of daily returns scaled to yearly)
volatility = data['Daily_Return'].std() * np.sqrt(252)
print("Annualized Volatility of INFY:", round(volatility, 4))

#  STEP 8: Compare Cumulative Returns of Strategy vs Buy & Hold
plt.figure(figsize=(12,6))
plt.plot(cumulative_stock, label="Buy & Hold INFY", color="blue")
plt.plot(cumulative_strategy, label="MA Crossover Strategy", color="orange")
plt.title("Strategy vs Stock Returns")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.grid(True)
plt.show()

#  STEP 9: Interactive Dashboard using Plotly
fig = go.Figure()

# Add traces for Close Price and Moving Averages
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close Price'))
fig.add_trace(go.Scatter(x=data.index, y=data['20_MA'], name='20-day MA'))
fig.add_trace(go.Scatter(x=data.index, y=data['50_MA'], name='50-day MA'))

# Customize layout
fig.update_layout(title="Infosys Stock Interactive Dashboard",
                  xaxis_title="Date",
                  yaxis_title="Price (INR)",
                  template="plotly_dark",
                  legend=dict(x=0, y=1))

fig.show()
