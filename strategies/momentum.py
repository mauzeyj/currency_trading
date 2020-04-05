# https://www.oreilly.com/content/algorithmic-trading-in-less-than-100-lines-of-python-code/


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from get_data.get_historical_data import get_data


def pips_difference(df):
    return df['closeAsk'] - df['closeAsk'].shift(1)


def close_ask_diff_momentum(df, average_bars: list):  # todo change to take a list
    strat_name = f'strategy_close_ask_diff_{average_bars}'
    strat = np.sign(df['pips'].rolling(average_bars).mean())
    return pd.Series(data=strat, name=strat_name)


def calc_returns(strategy_action_df, data_df):
    returns_df = pd.DataFrame
    # data_df['pips'] = pips_difference(data_df)
    for strat in list(strategy_action_df):
        returns_df[strat] = strategy_action_df[strat].shift(1) * data_df['pips']
    return returns_df


def aggregate_strategies(*argv):  # todo use config then argparse for this

    strategies = []
    for arg in argv:
        strategies.append(arg)
    return pd.concat(strategies, axis=1)


df = get_data()
df['pips'] = pips_difference(df)  # todo should I just put this in get_data()?

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


def

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
