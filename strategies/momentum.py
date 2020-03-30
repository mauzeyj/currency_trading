# https://www.oreilly.com/content/algorithmic-trading-in-less-than-100-lines-of-python-code/
# todo check to see how much it is trading
# todo change to go with best strategy
# todo change build strategy only with good data.
# should I do this in the data frame?  `
# todo track trades and profit

# todo strategy isn't shifting to the most profitable one correctly

"""
block each function and document and test. This shouldn't flail around so much
"""
import configparser

import matplotlib.pyplot as plt
import numpy as np
import oandapy as opy
import pandas as pd

from get_data.get_historical_data import get_data

df = get_data()

# todo account for slippage and trade fees
# (df['position_120'].diff() != 0).sum()
# df['returns'] = np.log(df['closeAsk'] / df['closeAsk'].shift(1))
# moved to actual pips. not sure why they were using log
df['returns'] = df['pips'] = df['closeAsk'] - df['closeAsk'].shift(1)
cols = []

strategies = pd.DataFrame()
# todo I think that I am creating my best strategy incorrectly or too soon
# todo create function that adds this momentum strategy   moving average momentum
# but the returns are off of the log
# todo pull these out to be parameters of class
for momentum in [15, 30, 60, 120]:
    col = 'strategy_%s' % momentum
    strategies[col] = np.sign(df['returns'].rolling(momentum).mean())
    cols.append(col)

strats = []
strategy_returns = pd.DataFrame()

for col in cols:
    strat = 'strategy_%s' % col.split('_')[1]
    # strat = f'strategy_{}' # fix previous code
    # todo add code to make columns based on if trade happened, enter value of trade fee in pips
    strategy_returns[strat] = strategies[col][120:].shift(1) * df['returns'][120:]
    strats.append(strat)

# best strategy
# fill na with 0?   what does this do?
strategies.fillna(0, inplace=True)
strategy_returns.fillna(0, inplace=True)


def apply_cumsum(df, window=0):
    new_df = df.dropna().cumsum().shift(window).apply(np.exp)
    return new_df


cumulative_returns = strategy_returns.dropna().cumsum()
best_strategy = cumulative_returns.idxmax(axis=1)

# best_strategy = strategy_returns.dropna().cumsum().idxmax(axis = 1) # .apply(np.exp)
best_action = []
"""
Something is happening between the best action and the returns. It is off by one or something. 
example 3 23 00 17    the best strategy is positive but the rest are negative. 

"""
# this needs to be going over the cumulative returns
for col, ind in zip(best_strategy.values, best_strategy.index.values):  # zeros towards beginning cut top of df?
    best_action.append(strategies.loc[ind, col])
strategies = strategies[120:]
strategies['best'] = best_action  # todo will want this set up for logging
strategy_returns['best'] = pd.Series(best_action).shift(1).values * df['returns'][120:]
cumulative_returns['best'] = strategy_returns['best'].cumsum()

# todo add fees df
big_df = pd.concat([strategies, cumulative_returns, df['returns'][120:]], axis=1)
big_df['best_action_return'] = strategy_returns['best']
big_df['best_strategy'] = best_strategy

# cumulative_returns = strategy_returns.dropna().cumsum().shift(0)#.apply(np.exp)
# cum_returns['best_strategy'] = cum_returns.idxmax(axis = 1)
# strategy_returns.dropna().cumsum().shift(0).plot() # .apply(np.exp)
cumulative_returns.plot()
plt.show()

config = configparser.ConfigParser()
oanda = opy.API(environment='practice',
                access_token=config['oanda']['access_token'])


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
