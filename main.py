import config
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time


# Function to fetch stock data from Alpha Vantage API
def fetch_stock_data(symbol):
    api_key = config.API_KEY
    if api_key is None:
        print("Error: API key not found in configuration")
        return None

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'Time Series (5min)' in data:
        df = pd.DataFrame(data['Time Series (5min)']).T
        df.index = pd.to_datetime(df.index)
        df = df.rename(
            columns={'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'})
        df = df.astype(float)
        return df
    else:
        print(f"Error: Data not available for {symbol}")
        return None


# Function to update and plot stock data for selected symbols
def update_and_plot(selected_symbols):
    while True:
        plt.figure(figsize=(12, 8))
        for i, symbol in enumerate(selected_symbols, start=1):
            plt.subplot(3, 4, i)
            df = fetch_stock_data(symbol)
            if df is not None:
                plt.plot(df.index, df['Close'], marker='o', linestyle='-', label=symbol)
                plt.title(f"Stock Price for {symbol}")
                plt.xlabel("Time")
                plt.ylabel("Price")
                plt.grid(True)
                plt.xticks(rotation=45)
                plt.legend()
        plt.tight_layout()
        plt.show()
        time.sleep(300)  # Update every 5 minutes


# Main function
def main():
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'NFLX', 'NVDA', 'INTC', 'AMD', 'IBM',
               'CSCO']  # Example stock symbols

    # Initialize the plot with the default symbols
    update_and_plot(symbols)


if __name__ == "__main__":
    main()
