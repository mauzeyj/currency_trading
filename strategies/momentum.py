# https://www.oreilly.com/content/algorithmic-trading-in-less-than-100-lines-of-python-code/


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from get_data.get_historical_data import get_data

"""
Get data and add pips columns - define
Generate strategies data frame
Generate returns data frame
Identify best strategy
Follow best strategy

"""


def pips_difference(df):
    return df['closeAsk'] - df['closeAsk'].shift(1)


def close_ask_diff_momentum(df, average_bars):  # todo change to take a list
    strat_name = f'strategy_close_ask_diff_{average_bars}'
    strat = np.sign(df['pips'].rolling(average_bars).mean())
    return pd.Series(data=strat, name=strat_name)


def calc_returns(strategy_action_df, data_df):
    returns_df = pd.DataFrame()
    # data_df['pips'] = pips_difference(data_df)
    for strat in list(strategy_action_df):
        returns_df[strat] = strategy_action_df[strat].shift(1) * data_df['pips']
    return returns_df


def aggregate_strategies(*argv):  # todo use config then argparse for this
    strategies = []
    for arg in argv:
        strategies.append(arg)
    return pd.concat(strategies, axis=1)


def cumulative_sum(df, window=0):
    new_df = df.dropna().cumsum().shift(window)  # .apply(np.exp)  # todo drop na or fillna?
    return new_df


def returns_df():
    pass


def plot_strategy_returns(cumulative_returns_df):
    cumulative_returns_df.plot()
    plt.show()


def fees_df(strategies_df):
    np.where(strategies_df != strategies_df.shift(1), .00001)  # something like this


def plot_strategy_trade_amount():
    # maybe a candle stick of each strategies buys and sells
    pass


def cummulative_gains_best_strategy(strategies_df, returns_df):  # this strategy doesn't work
    strategies_df.fillna(0, inplace=True)
    returns_df.fillna(0, inplace=True)
    cumulative_returns = cumulative_sum(returns_df)
    best_strategy = cumulative_returns.idxmax(axis=1)
    return best_strategy


def identify_best_action(strategies, best_strategy):
    best_action = []
    for col, ind in zip(best_strategy.values, best_strategy.index.values):  # zeros towards beginning cut top of df?
        best_action.append(strategies.loc[ind, col])
    return best_action


def rolling_average_cummulative_gains_best_strategy(strategies_df, returns_df, window):
    strategies_df.fillna(0, inplace=True)
    returns_df.fillna(0, inplace=True)
    cumulative_returns = returns_df.dropna().rolling(window).mean()
    best_strategy = cumulative_returns.idxmax(axis=1)
    return best_strategy


# gets data and does formatting
df = get_data()
df['pips'] = pips_difference(df)  # todo should I just put this in get_data()?

# creates strategies  and returns df
strategies = aggregate_strategies(close_ask_diff_momentum(df, 5), close_ask_diff_momentum(df, 10))
returns = calc_returns(strategies, df)

# creates cumulative sum table
cumulative_returns_df = cumulative_sum(returns)

# identifies best action based on best action strategy
best_strategy = cummulative_gains_best_strategy(strategies, returns)
# best_strategy = rolling_average_cummulative_gains_best_strategy(strategies, returns, 5)
strategies['best_action_return'] = identify_best_action(strategies,
                                                        best_strategy)
# calculates returns again with new strategy added and recreates cumulative sum table
returns = calc_returns(strategies, df)
cumulative_returns_df = cumulative_sum(returns)

# puts everything into a big table for analysis
big_df = pd.concat([df['pips'], returns, strategies, cumulative_returns_df],
                   axis=1)  # todo create big df to make sure this is working
big_df['diff_best_5'] = big_df.iloc[:, -3] - big_df.iloc[:, -1]
big_df['diff_best_10'] = big_df.iloc[:, -3] - big_df.iloc[:, -2]
big_df['best_strat'] = best_strategy
plot_strategy_returns(cumulative_returns_df)
