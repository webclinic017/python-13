from binance import Client
import pandas as pd
import personal_function as pf
import numpy as np

client=pf.client()
trade_history_df, summary_df=pf.summary('Trade_History.xlsx')
print(trade_history_df)
print(summary_df)

#print(symbols)