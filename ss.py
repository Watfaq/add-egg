import os
import json
import BaseHTTPServer
import requests

KRAKEN_API = 'https://api.kraken.com/0/public/Ticker'
EOS_PAIR = 'EOSXBT'
XBT_PAIR = 'XXBTZUSD'
CURRENCY_API = 'https://api.fixer.io/latest'


def get_eos_to_usd():
    eos_ask = requests.get(KRAKEN_API, params={'pair': EOS_PAIR}).json()[
        'result'][EOS_PAIR]['a'][0]
    xbt_ask = requests.get(KRAKEN_API, params={'pair': XBT_PAIR}).json()[
        'result'][XBT_PAIR]['a'][0]
    usd_rates = requests.get(
        CURRENCY_API,
        params={'base': 'USD', 'symbols': 'CNY,EUR'}
    ).json()['rates']

    eos_to_usd = float(eos_ask) * float(xbt_ask)
    eos_to_cny = eos_to_usd * usd_rates['CNY']
    eos_to_eur = eos_to_usd * usd_rates['EUR']

    return locals()


class IndexHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        s.send_response(200)
        s.send_header('Content-Type', 'application/json')
        s.end_headers()
        s.wfile(json.dumps(get_eos_to_usd()))


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(('', os.environ.get('PORT')), IndexHandler)
    httpd.serve_forever()
