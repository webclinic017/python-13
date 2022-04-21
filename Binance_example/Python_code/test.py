from binance import Client
import personal_function as pf
import pandas as pd

client=pf.client()
tickers=client.get_all_tickers()
tickers_df= pd.DataFrame(tickers)
tickers_df.set_index('symbol',inplace=True)
#print(tickers_df)

KlinesType ='SPOT'
symbol ='ETHBTC'
interval = '1d' # 30m, 4h,8h,12h,3d,1w
start_date ='1 Jan 2011'
end_date = '1 Jan 2021'
#limit = 500
hist_df=pf.historical_data(client,symbol, interval, start_date, end_date, KlinesType)
print(hist_df.dtypes)
