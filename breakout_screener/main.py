#modules
from calendar import c
from logging.config import valid_ident
import pandas as pd
import personal_function as pf
from datetime import datetime
import csv
from binance import Client
from binance.enums import HistoricalKlinesType

#functions
def is_consolidating(df, period=20,percentage=2):
    """
    This function is to check whether a coin is consolidating
    """
    recent_candlesticks = df[-period:]
    max_close = recent_candlesticks['Close'].max()
    min_close = recent_candlesticks['Close'].min()

    threshold = 1 - (percentage / 100)
    if min_close > (max_close * threshold):
        return True        

    return False

"""
#The first_prototype of breakout
def is_breaking_out(df, period,percentage=2.5):
    last_close = df[-1:]['Close'].values[0]

    if is_consolidating(df[:-1], percentage=percentage):
        recent_closes = df[-(period+1):-1]

        if last_close > recent_closes['Close'].max():
            return True

    return False
"""

#The second prototype of breakout
def is_breaking_out(df, consolidate_period,breakout_period,percentage=2.5):
    """
    This function is to check a coin is breaking out 
    """
    last_closes = df[-breakout_period:]['Close']
    last_closes=last_closes.to_numpy()

    #print(last_closes)
    if is_consolidating(df[:-breakout_period], percentage=percentage):
        recent_closes = df[-(breakout_period+consolidate_period):-breakout_period]
        #print(recent_closes)
        if (last_closes.min() > recent_closes['Close'].max()) or last_closes.max() < recent_closes['Close'].min():
            return True
    return False



#variables
pair='USDT'
exist_symbols=[]
consolidating=[]
breaking_out=[]
start_date='1 Jan 2022'
now = datetime.now()
end_date=now.strftime("%d %b %Y %H:%M:%S")
period=14
percentage=15
consolidate_period=14
breakout_period=3

#main
client=pf.client()
tickers = client.get_all_tickers()
tickers_df=pd.DataFrame(tickers)

#get all the existed USDT pairs
for symbol in tickers_df['symbol']:
    if pair in symbol:
        exist_symbols.append(symbol)
valid_symbols=exist_symbols

#print(type(valid_symbols))
#KlinesType ='SPOT'
#symbol_test ='BTCUSDT'
#interval = '12h'


#For some reasons I dont know, there are USDT pairs that exist but don't have historical data.
for symbol in exist_symbols:
    print(symbol)
    historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_12HOUR, start_date, end_date,\
        klines_type = HistoricalKlinesType.SPOT)
    if len(historical)==0:
        # This function is to remove them.
        print('the data of {} is incorrect'.format(symbol))
        valid_symbols.remove(symbol)
        continue

    #This function is to clean up the mess and put the historical data into pandas data frame/
    hist_df=pd.DataFrame(historical)
    hist_df.columns = ['Open Time','Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',\
                'Quote Asset Volume', 'Number of Trades', 'TB Base Volume','TB Quote Volume','Ignore']
    hist_df['Open Time'] = pd.to_datetime(hist_df['Open Time']/1000, unit = 's')
    hist_df['Close Time'] = pd.to_datetime(hist_df['Close Time']/1000, unit = 's')
    numeric_columns=['Open', 'High', 'Low', 'Close', 'Volume',\
                    'Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']
    hist_df[numeric_columns]=hist_df[numeric_columns].apply(pd.to_numeric,axis=1)
    hist_df.drop(columns=['Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume','Close Time','Ignore','Number of Trades'], inplace=True)
    #hist_df.to_csv('{}.csv'.format(symbol))
    
    """
    #This function is to check consolidating.
    if is_consolidating(hist_df, period,percentage):
        consolidating.append(symbol)
        print("{} is consolidating".format(symbol))
    """
    #This function is to check for breakout
    if is_breaking_out(hist_df,consolidate_period,breakout_period,percentage):
        breaking_out.append(symbol)
        print("{} is breaking out".format(symbol))

with open('consolidating.csv','w') as f:
    write = csv.writer(f)
    write.writerow(consolidating)

with open('breaking_out.csv','w') as f:
    write = csv.writer(f)
    write.writerow(breaking_out)

with open('valid_symbols.csv','w') as f:
    write = csv.writer(f)
    write.writerow(valid_symbols)
