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

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from get_data.get_historical_data import get_data

df = get_data()

def close_ask_diff_momentum(data, average_bars):


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
