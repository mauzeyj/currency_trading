# https://www.oreilly.com/content/algorithmic-trading-in-less-than-100-lines-of-python-code/


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# import seaborn as sns; sns.set()
from get_data.get_historical_data import get_bar_data

# data = oanda.get_history(instrument='EUR_USD',  # our instrument
#                          start='2016-12-08',  # start data
#                          end='2016-12-10',  # end date
#                          granularity='M1')  # minute bars  # 7

data = get_bar_data().json()
df = pd.DataFrame(data['candles']).set_index('time')

df.index = pd.DatetimeIndex(df.index)

df.info()

# todo account for slippage and trade fees
df['returns'] = np.log(df['closeAsk'] / df['closeAsk'].shift(1))

cols = []

for momentum in [15, 30, 60, 120]:
    col = 'position_%s' % momentum
    df[col] = np.sign(df['returns'].rolling(momentum).mean())
    cols.append(col)

strats = ['returns']

for col in cols:
    strat = 'strategy_%s' % col.split('_')[1]
    df[strat] = df[col].shift(1) * df['returns']
    strats.append(strat)  # 23

df[strats].dropna().cumsum().apply(np.exp).plot()
plt.show()
