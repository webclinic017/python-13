import csv
from binance.client import Client
import personal_function as pf
from datetime import datetime
import pandas as pd
client = pf.Client()

# prices = client.get_all_tickers()

# for price in prices:
#     print(price)

csvfile = open('backtest_data.csv', 'w', newline='') 
candlestick_writer = csv.writer(csvfile, delimiter=',')

candlesticks = client.get_historical_klines("SOLUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 Jan, 2021", "31 Dec, 2021")
#candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2020", "12 Jul, 2020")
#candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2017", "12 Jul, 2020")

for candlestick in  candlesticks:
    candlestick[0] = int(candlestick[0]/1000)
    #candlestick[0]=datetime.utcfromtimestamp(candlestick[0]).strftime('%Y-%m-%d %H:%M:%S')
    candlestick_writer.writerow(candlestick)

csvfile.close()