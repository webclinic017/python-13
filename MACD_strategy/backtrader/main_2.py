# %%
from binance import Client
import personal_function as pf
import pandas as pd
import numpy as np
import mplfinance as mpf
from binance.enums import *
import datetime  # For datetime objects
import sys  # To find out the script name (in argv[0])
import backtrader as bt

# %%
client=pf.client()

KlinesType ='SPOT'
symbol ='BTCUSDT'
interval = '4h' # 30m, 4h,8h,12h,3d,1w
start_date ='1 Jan 2011'
end_date = '1 Jan 2021'
#limit = 500
hist_df=pf.historical_data(client,symbol, interval, start_date, end_date, KlinesType)

# %%
training_df=hist_df[0:int((hist_df.shape[0]/2))+1]
training_df.to_csv('{}_training.csv'.format(symbol))
test_df=hist_df[int((hist_df.shape[0]/2))+1:]
test_df.to_csv('{}_test.csv'.format(symbol))

# %%
class MACD(bt.Strategy):
    '''
    This strategy is loosely based on some of the examples from the Van
    K. Tharp book: *Trade Your Way To Financial Freedom*. The logic:

      - Enter the market if:
        - The MACD.macd line crosses the MACD.signal line to the upside
        - The Simple Moving Average has a negative direction in the last x
          periods (actual value below value x periods ago)

     - Set a stop price x times the ATR value away from the close

     - If in the market:

       - Check if the current close has gone below the stop price. If yes,
         exit.
       - If not, update the stop price if the new stop price would be higher
         than the current
    '''

    params = (
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('atrperiod', 14),  # ATR Period (standard)
        ('atrdist', 3.0),   # ATR distance for stop price
        ('smaperiod', 30),  # SMA Period (pretty standard)
        ('dirperiod', 10),  # Lookback period to consider SMA trend direction
    )

    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None  # indicate no order is pending

    def __init__(self):
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.p.macd1,
                                       period_me2=self.p.macd2,
                                       period_signal=self.p.macdsig)

        # Cross of macd.macd and macd.signal
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

        # To set the stop price
        self.atr = bt.indicators.ATR(self.data, period=self.p.atrperiod)

        # Control market trend
        self.sma = bt.indicators.SMA(self.data, period=self.p.smaperiod)
        self.smadir = self.sma - self.sma(-self.p.dirperiod)

    def start(self):
        self.order = None  # sentinel to avoid operrations on pending order

    def next(self):
        if self.order:
            return  # pending order execution

        if not self.position:  # not in the market
            if self.mcross[0] > 0.0 and self.smadir < 0.0:
                self.order = self.buy()
                pdist = self.atr[0] * self.p.atrdist
                self.pstop = self.data.close[0] - pdist

        else:  # in the market
            pclose = self.data.close[0]
            pstop = self.pstop

            if pclose < pstop:
                self.close()  # stop met - get out
            else:
                pdist = self.atr[0] * self.p.atrdist
                # Update only if greater than
                self.pstop = max(pstop, pclose - pdist)

# %%
if __name__ == '__main__':
    data=bt.feeds.GenericCSVData(
    dataname='{}_training.csv'.format(symbol),
    fromdate=datetime.datetime(2017,8,17,4,0,0),
    todate=datetime.datetime(2019,4,26,8,0,0),
    datetime=1,
    open=2,
    high=3,
    low=4,
    close=5,
    volume=6,
    dtformat=('%Y-%m-%d %H:%M:%S'),
    tmformat=('%H:%M:%S'),
    timeframe=bt.feeds.TimeFrame.Ticks
)
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MACD)
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
    cerebro.addsizer(bt.sizers.SizerFix, stake=30)


    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    thestrats=cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    thestrat = thestrats[0]
    print('Sharpe Ratio:',  thestrat.analyzers.mysharpe.get_analysis())
    cerebro.plot()
    


