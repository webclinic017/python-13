import backtrader as bt
import datetime
#import sys

class RSIStrategy(bt.Strategy):
    #params = (('period', 20),)
    def log(self, txt, dt=None):
        #Print function
        dt = dt or self.datas[0].datetime.datetime(0)
        with open('results.txt', 'a') as f:
            f.write('%s, %s' % (dt.isoformat(), txt))
            f.write('\n')
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Initializing...
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.rsi = bt.talib.RSI(self.data, timeperiod=RSI_period)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        global profit
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
        profit=profit+trade.pnlcomm
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        

    def next(self):
        #self.log('Close, %.2f' % self.dataclose[0])
        if self.order:
            return
        
        if not self.position:
            if self.rsi < oversold and not self.position:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order=self.buy()
        
        else:
            if self.rsi > overbought and self.position:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order=self.sell()


#variables

#For cerebro
data_name='backtest_data.csv'
slip_perc=0.005 
set_cash=1000 
set_commission=0.001
profit=0

#For RSI
RSI_period=20
overbought=70
oversold=30

#main
open("results.txt", "w").close() #to erase all the information from the previous run

#initialize cerebro
cerebro = bt.Cerebro()
data = bt.feeds.GenericCSVData(
    dataname=data_name, 
    dtformat=2, 
    #compression=15, 
    timeframe=bt.TimeFrame.Minutes,
    )
cerebro.addstrategy(RSIStrategy)
cerebro.broker = bt.brokers.BackBroker(slip_perc=slip_perc,slip_open=True,slip_match=True, slip_out=False)
cerebro.adddata(data)
cerebro.broker.setcash(set_cash)
cerebro.broker.setcommission(commission=set_commission)
cerebro.addsizer(bt.sizers.FixedSize, stake=1)

print("The commission is {}% and the slippage is {}%.".format(set_commission*100,slip_perc*100))
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('The overall profit: %.2f' %profit)
#note that we can see the difference between the final and the intial portfolio is not equal
#to the overall profit. It is because the final executation is a BUY. 
#so the final portfolio is cash+ the price of the stock of the last price - the last commission fee.
cerebro.plot()