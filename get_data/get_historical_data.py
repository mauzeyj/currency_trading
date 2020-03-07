from requests import get

import config

# todo document these examples
conf = config.conf

ob = get("https://api-fxtrade.oanda.com/v3/instruments/USD_JPY/orderBook",
         headers={'Authorization': 'Bearer ' + conf['Bearer']})

c = get("https://api-fxtrade.oanda.com/labs/v1/calendar?instrument=EUR_USD&period=2592000",
        headers={'Authorization': 'Bearer ' + conf['Bearer']})


# todo set time frame to most current and parameterize
def get_bar_data(instrument='EUR_USD', count='500', granularity='M'):
    ca = get(
        f"https://api-fxtrade.oanda.com/v1/candles?instrument={instrument}&count={count}&granularity={granularity}&alignmentTimezone=America%2FNew_York")
    return ca


ac = get("https://api-fxtrade.oanda.com/labs/v1/signal/autochartist?instrument=EUR_CAD&period=604800type=keylevel",
         headers={'Authorization': 'Bearer ' + conf['Bearer']})

t = get('https://api-fxtrade.oanda.com/v3/instruments/EUR_USD/candles?count=5000&price=M&granularity=M1',
        headers={'Authorization': 'Bearer ' + conf['Bearer']})
