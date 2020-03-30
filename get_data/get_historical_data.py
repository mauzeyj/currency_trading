import configparser

import oandapy as opy
import pandas as pd


def get_data(instrument='EUR_USD', start='2020-03-22', end='2020-03-24', granularity='M1'):
    config = configparser.ConfigParser()
    config.read('oanda.cfg')

    oanda = opy.API(environment='practice',
                    access_token=config['oanda']['access_token'])

    data = oanda.get_history(instrument=instrument,  # our instrument
                             start=start,  # start data
                             end=end,  # end date
                             granularity=granularity)  # minute bars

    df = pd.DataFrame(data['candles']).set_index('time')

    df.index = pd.DatetimeIndex(df.index)
