# For some reasons that I don't know, client.get_all_tickers() gives me some bitcoins
#which do not exist. This program is to find them and remove them from the list of symbols.


#modules
import pandas as pd
import personal_function as pf
from datetime import datetime
from binance import Client
from binance.enums import HistoricalKlinesType
import csv

#main

client=pf.client()
prices = client.get_all_tickers()
prices_df=pd.DataFrame(prices)
pair='USDT'
search_symbol=[]
for symbol in prices_df['symbol']:
    if pair in symbol:
        search_symbol.append(symbol)
print(len(search_symbol))


start_date='1 Jan 2022'
now = datetime.now()
end_date=now.strftime("%d %b %Y %H:%M:%S")
KlinesType ='SPOT'
symbol_test ='BTCUSDT'
interval = '12h'


for symbol in search_symbol:
    candles=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_12HOUR, start_date, end_date,\
        klines_type = HistoricalKlinesType.SPOT)
    if len(candles)==0:
        search_symbol.remove(symbol)

with open('valid_symbol.csv','w') as f:
    write = csv.writer(f)
    write.writerow(search_symbol)
print(len(search_symbol))