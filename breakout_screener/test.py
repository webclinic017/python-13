#modules
from calendar import c
from logging.config import valid_ident
import pandas as pd
import personal_function as pf
from datetime import datetime
import csv
from binance import Client
from binance.enums import HistoricalKlinesType


def is_consolidating(df, period=20,percentage=2):
    recent_candlesticks = df[-period:]
    print(recent_candlesticks)
    max_close = recent_candlesticks['Close'].max()
    min_close = recent_candlesticks['Close'].min()

    threshold = 1 - (percentage / 100)
    if min_close > (max_close * threshold):
        return True        

    return False

def is_breaking_out(df, consolidate_period,breakout_period,percentage=2.5):
    last_closes = df[-breakout_period:]['Close']
    last_closes=last_closes.to_numpy()
    print(last_closes)
    if is_consolidating(df[:-breakout_period], percentage=percentage):
        recent_closes = df[-(breakout_period+consolidate_period):-breakout_period]
        print(recent_closes)
        if last_closes.min() > recent_closes['Close'].max():
            return True
    return False
    
    """
    if last_closes.min() > recent_closes.max():
        return True
    return False

    print('last closes: {}'.format(last_closes))
    print('recent closes: {}'.format(recent_closes))
    """


pair='USDT'
exist_symbols=[]
consolidating=[]
breaking_out=[]
start_date='1 Jan 2022'
now = datetime.now()
end_date=now.strftime("%d %b %Y %H:%M:%S")
period=28
consolidating_period=28
breakout_period=3
percentage=5
symbol='GLMRUSDT'

client=pf.client()
historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_12HOUR, start_date, end_date,\
    klines_type = HistoricalKlinesType.SPOT)
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


#is_consolidating(hist_df, period,percentage)
 

is_breaking_out(hist_df,consolidating_period,breakout_period,percentage)
    #breaking_out.append(symbol)
    #print("{} is breaking out".format(symbol))

