import configparser

import oandapy as opy
import pandas as pd


# todo document these examples
# conf = config.conf

# ob = get("https://api-fxtrade.oanda.com/v3/instruments/USD_JPY/orderBook",
#          headers={'Authorization': 'Bearer ' + conf['Bearer']})
#
# c = get("https://api-fxtrade.oanda.com/labs/v1/calendar?instrument=EUR_USD&period=2592000",
#         headers={'Authorization': 'Bearer ' + conf['Bearer']})
#
#
# # todo set time frame to most current and parameterize
# def get_bar_data(instrument='EUR_USD', count='500', granularity='M'):
#     ca = get(
#         f"https://api-fxtrade.oanda.com/v1/candles?instrument={instrument}&count={count}&granularity={granularity}&alignmentTimezone=America%2FNew_York")
#     return ca
#
#
# ac = get("https://api-fxtrade.oanda.com/labs/v1/signal/autochartist?instrument=EUR_CAD&period=604800type=keylevel",
#          headers={'Authorization': 'Bearer ' + conf['Bearer']})
#
# t = get('https://api-fxtrade.oanda.com/v3/instruments/EUR_USD/candles?count=5000&price=M&granularity=M1',
#         headers={'Authorization': 'Bearer ' + conf['Bearer']})

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
