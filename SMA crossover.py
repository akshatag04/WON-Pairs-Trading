import sqlite3
import backtrader as bt
import pandas as pd
from datetime import datetime

df1 = pd.read_csv('data.csv')
df1['tradedate'] = pd.to_datetime(df1['tradedate'], format= '$Y$m$d')
df2 = df1.groupby('symbol')

rel = df2.get_group('REL.IN')
ilc = df2.get_group('ILC.IN')
hds = df2.get_group('HDS.IN')
wip = df2.get_group('WIP.IN')

cerebro = bt.Cerebro()
cerebro.broker.setcash(1000000.0)
cerebro.broker.getcash()

class TestStrategy(bt.Strategy):
    params = (
    ('fast', 50),
    ('slow', 200)
    )

    def __init__(self):
        self.crossovers = [ ]
        self.orders_ = [ ]
        self.bars_executed = [None, None, None, None]

        for d in self.datas:
            ma_fast = bt.ind.SMA(d, period = self.params.fast)
            ma_slow = bt.ind.SMA(d, period = self.params.slow)
            self.order =  None
            self.orders_.append(self.order)
            self.crossover =  bt.ind.CrossOver(ma_fast, ma_slow)
            self.crossovers.append(bt.ind.CrossOver(ma_fast, ma_slow))

    def notify_order(self, order):
        for i,d in enumerate(self.datas):
            order = self.orders_ [i]
            if order.status in [order. Submitted, order.Accepted]: 
                continue
            if order.status in [order.Completed]:
                if order.isbuy():
                    self.bar_executed = len(self)
                    self.bars_executed[i] = self.bar_executed
                elif order.issell():
                    self.bar_executed = len(self)
                    self.bars_executed[i] = self.bar_executed

    def next (self):

        money = cerebro.broker.getcash()
        for i,d in enumerate(self. datas):
            cerebro.broker.setcash(money/4) 
            if (self.getposition(d).size == 0):
                if self.crossovers[i] > 0:
                    self.orders_[i] = self.buy(data = d) 
                elif self.crossovers[i] < 0:
                    self.orders_[i]= self.sell(data = d)

        else:               
            if len(self) >= (self.bars_executed[i] + 5):
                self.orders_[i] = self.close(data = d)
    
   

class PandasData(bt.feed.DataBase) :
    params = (
        ('datetime' 'tradedate'),
        ('open','close')
        ('high',  'close')
        ('low', ' close')
        ('close',  'close')
        ('volume',  None),
        ('openinterest', None)
        )

stocks = {'rel':rel, 'ilc':ilc, 'hds':hds, 'wip':wip}
cerebro.addstrategy(TestStrategy)
for s in stocks:
    data = bt.feeds.PandasData(dataname = stocks[s], datetime = 'tradedate', close = 'close', open = 'close', high = 'close', low = 'close', volume = None, openinterest = None)
    cerebro.adddata(data, name = s)

cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'sharpe')
cerebro.addanalyzer(bt.analyzers.Returns, _name = 'returns')
test = cerebro.run(runonce = False)
cerebro.plot(volume = False)
