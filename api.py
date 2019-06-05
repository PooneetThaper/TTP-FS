import requests

def get_price(ticker):
    return requests.get('https://api.iextrading.com/1.0/stock/{}/price'.format(ticker))

def get_open_high_low_close(ticker):
    return requests.get('https://api.iextrading.com/1.0/stock/{}/ohlc'.format(ticker))

def batch_get_info(tickers, endpoints):
    return requests.get('https://api.iextrading.com/1.0/stock/market/batch?symbols={}&types={}'.format(",".join(tickers), ",".join(endpoints)))
