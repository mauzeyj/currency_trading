# https://www.oreilly.com/content/algorithmic-trading-in-less-than-100-lines-of-python-code/
# todo check to see how much it is trading
# todo change to go with best strategy
# should I do this in the data frame?  `
# todo track trades and profit

import configparser

import matplotlib.pyplot as plt
import numpy as np
import oandapy as opy
import pandas as pd

config = configparser.ConfigParser()
config.read('oanda.cfg')

oanda = opy.API(environment='practice',
                access_token=config['oanda']['access_token'])

data = oanda.get_history(instrument='EUR_USD',  # our instrument
                         start='2020-03-22',  # start data
                         end='2020-03-24',  # end date
                         granularity='M1')  # minute bars

df = pd.DataFrame(data['candles']).set_index('time')

df.index = pd.DatetimeIndex(df.index)

df.info()

# todo account for slippage and trade fees
# (df['position_120'].diff() != 0).sum()
df['returns'] = np.log(df['closeAsk'] / df['closeAsk'].shift(1))

cols = []

strategies = pd.DataFrame()

# todo create function that adds this momentum strategy   moving average momentum
# but the returns are off of the log
for momentum in [15, 30, 60, 120]:
    col = 'position_%s' % momentum
    strategies[col] = np.sign(df['returns'].rolling(momentum).mean())
    cols.append(col)

strats = []

strategy_returns = pd.DataFrame()

for col in cols:
    strat = 'strategy_%s' % col.split('_')[1]
    # strat = f'strategy_{}' # fix previous code
    # todo add code to make columns based on if trade happened, 863393  enter value of trade fee in pips
    strategy_returns[strat] = strategies[col].shift(1) * df['returns']
    strats.append(strat)

strategy_returns[strats].dropna().cumsum().apply(np.exp).plot()
plt.show()


class MomentumTrader(opy.Streamer):
    def __init__(self, momentum, *args, **kwargs):
        opy.Streamer.__init__(self, *args, **kwargs)
        self.ticks = 0
        self.position = 0
        self.df = pd.DataFrame()
        self.momentum = momentum
        self.units = 100000

    def create_order(self, side, units):  # 33
        order = oanda.create_order(config['oanda']['account_id'],
                                   instrument='EUR_USD', units=units, side=side,
                                   type='market')  # 34
        print('\n', order)  # 35

    def on_success(self, data):  # 36
        self.ticks += 1  # 37
        # print(self.ticks, end=', ')
        # appends the new tick data to the DataFrame object
        self.df = self.df.append(pd.DataFrame(data['tick'],
                                              index=[data['tick']['time']]))  # 38
        # transforms the time information to a DatetimeIndex object
        self.df.index = pd.DatetimeIndex(self.df['time'])  # 39
        # resamples the data set to a new, homogeneous interval
        dfr = self.df.resample('5s').last()  # 40
        # calculates the log returns
        dfr['returns'] = np.log(dfr['ask'] / dfr['ask'].shift(1))  # 41
        # derives the positioning according to the momentum strategy
        dfr['position'] = np.sign(dfr['returns'].rolling(
            self.momentum).mean())  # 42
        if dfr['position'].ix[-1] == 1:  # 43
            # go long
            if self.position == 0:  # 44
                self.create_order('buy', self.units)  # 45
            elif self.position == -1:  # 46
                self.create_order('buy', self.units * 2)  # 47
            self.position = 1  # 48
        elif dfr['position'].ix[-1] == -1:  # 49
            # go short
            if self.position == 0:  # 50
                self.create_order('sell', self.units)  # 51
            elif self.position == 1:  # 52
                self.create_order('sell', self.units * 2)  # 53
            self.position = -1  # 54
        if self.ticks == 250:  # 55
            # close out the position
            if self.position == 1:  # 56
                self.create_order('sell', self.units)  # 57
            elif self.position == -1:  # 58
                self.create_order('buy', self.units)  # 59
            self.disconnect()  # 60
