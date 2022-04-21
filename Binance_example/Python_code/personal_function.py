from unicodedata import name
from binance import Client
from matplotlib.pyplot import hist
from binance.enums import HistoricalKlinesType
import pandas as pd

def client():
    apikey='MZoUNKZin6hLFAaPtMyi0GrZXjz8ca55OL4Qlmys3YuUOSzS6fdtW97WvlKzs5yA'
    secret='QuIoCo9pTkb8hw1ktIXZoxtPKnG9e2kXYCLy05c876aHqA4NL1T4s5ZAWtD2q9y4'
    return Client(apikey, secret)

def historical_data(client, symbol,interval, start_date, end_date,KlinesType):
    if KlinesType=='SPOT':
        if interval=='30m':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_30MINUTE, start_date, end_date,\
            klines_type = HistoricalKlinesType.SPOT)
        elif interval=='4h':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_4HOUR, start_date, end_date,\
            klines_type = HistoricalKlinesType.SPOT)
        elif interval=='8h':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_8HOUR, start_date, end_date,\
            klines_type = HistoricalKlinesType.SPOT)
        elif interval=='12h':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_12HOUR, start_date, end_date,\
            klines_type = HistoricalKlinesType.SPOT)
        elif interval=='1d':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_date, end_date,\
            klines_type = HistoricalKlinesType.SPOT)
        elif interval=='3d':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_3DAY, start_date, end_date,\
            klines_type = HistoricalKlinesType.SPOT)
        elif interval=='1w':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1WEEK, start_date, end_date,\
            klines_type = HistoricalKlinesType.SPOT)
        else:
            return 0;
        
    elif KlinesType=='FUTURES':
        if interval=='30m':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_30MINUTE, start_date, end_date,\
            klines_type = HistoricalKlinesType.FUTURES)
        elif interval=='4h':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_4HOUR,start_date, end_date,\
            klines_type = HistoricalKlinesType.FUTURES)
        elif interval=='8h':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_8HOUR,start_date, end_date,\
            klines_type = HistoricalKlinesType.FUTURES)
        elif interval=='12h':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_12HOUR,start_date, end_date,\
            klines_type = HistoricalKlinesType.FUTURES)
        elif interval=='1d':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY,start_date, end_date,\
            klines_type = HistoricalKlinesType.FUTURES)
        elif interval=='3d':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_3DAY,start_date, end_date,\
            klines_type = HistoricalKlinesType.FUTURES)
        elif interval=='1w':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1WEEK,start_date, end_date,\
            klines_type = HistoricalKlinesType.FUTURES)
        else:
            return 0;
    else:
        return 0;
    hist_df=pd.DataFrame(historical)
    hist_df.columns = ['Open Time','Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',\
                'Quote Asset Volume', 'Number of Trades', 'TB Base Volume','TB Quote Volume','Ignore']
    hist_df['Open Time'] = pd.to_datetime(hist_df['Open Time']/1000, unit = 's')
    hist_df['Close Time'] = pd.to_datetime(hist_df['Close Time']/1000, unit = 's')
    numeric_columns=['Open', 'High', 'Low', 'Close', 'Volume',\
                    'Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']
    hist_df[numeric_columns]=hist_df[numeric_columns].apply(pd.to_numeric,axis=1)
    hist_df.to_csv('{}.csv'.format(symbol))
    return hist_df


