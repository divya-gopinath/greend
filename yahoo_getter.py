from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import time
import pickle

YAHOO_FINANCE_URL = 'https://finance.yahoo.com/quote/{t}/sustainability?p={t}'
WAIT_TIME_BTWN_REQS = 0.1  # seconds


def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if valid_html(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def valid_html(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def cacheify(cache):
    try:
        cache_data = pickle.load(open('{}.p'.format(cache), 'rb'))
    except FileNotFoundError:
        cache_data = {}

    def cacheify_decorator(func):
        def wrapper(arg):
            if arg in cache_data.keys():
                return cache_data[arg]
            else:
                ret_val = func(arg)
                cache_data[arg] = ret_val
                pickle.dump(cache_data, open('{}.p'.format(cache), 'wb'))
                return ret_val
        return wrapper
    return cacheify_decorator


@cacheify('esg_cache')
def scrape_esg(ticker):
    esg = {'env': None, 'soc': None, 'gov': None}
    url = YAHOO_FINANCE_URL.format(t=ticker)
    time.sleep(WAIT_TIME_BTWN_REQS)
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    for div in html.select('div'):
        if div.attrs.get('data-reactid', 0) == '35':
            esg['env'] = float(div.text)
        elif div.attrs.get('data-reactid', 0) == '45':
            esg['soc'] = float(div.text)
        elif div.attrs.get('data-reactid', 0) == '55':
            esg['gov'] = float(div.text)
    return esg


if __name__ == '__main__':
    print(scrape_esg('FB'))
    print(scrape_esg('FB'))
    print(scrape_esg('AAPL'))
