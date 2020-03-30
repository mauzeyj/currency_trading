import configparser

import oandapy as opy
import pandas as pd


def get_data(instrument='EUR_USD', start='2020-03-22', end='2020-03-24', granularity='M1'):
    """
    Retrieves data from Oanda, puts candles data into pandas dataframe, sets index to time
    :param instrument: string: instrument that data is requested for ex
    :param start: string: year-month-day for the data to start
    :param end: string: year-month-day for the data to end
    :param granularity: code for the granularity #todo get a list of these and provide them
    :return: pandas dataframe
    """
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
