# encoding: utf-8
import os

from apscheduler.schedulers.blocking import BlockingScheduler

import requests

MAILGUN_KEY = os.environ.get('MAILGUN_KEY')


sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=12)
def add_egg():
    print(send_mail(get_text(get_price())))


@sched.scheduled_job('interval', minutes=1)
def calc_lost_money():
    price = get_price()
    sell = price['sell']
    lost = _calc_lost_money(float(sell))

    print('Current lost %s, current sell price %s' % (lost, sell))

    if lost > 30000:
        send_mail('Lost > %s' % lost)

    if lost < -5000:
        send_mail('Win 5k!!!!!!!!')
        send_mail('Win 5k!!!!!!!!')
        send_mail('Win 5k!!!!!!!!')


def _calc_lost_money(x):
    return ((16.72 - x) / 16.72 + 0.0002) * 40000


def get_price():
    r = requests.get('https://yunbi.com/api/v2/tickers').json()
    eos = r['eoscny']
    return eos['ticker']


def get_text(price):
    kwargs = price.copy()
    kwargs['lost'] = _calc_lost_money(float(price['sell']))

    return '''
Cool!

Eos Sumary:
    Buy: {buy}
    Sell: {sell},
    Low: {low},
    High: {high},
    Last: {last},
    Vol: {vol},
    Lost: {lost}

Add an egg for your lunch!

'''.format(**kwargs)


def send_mail(text):
    api_host = 'https://api.mailgun.net/v3/noreply.watfaq.com/messages'
    token = MAILGUN_KEY

    sender = 'NoReply <no-reply@noreply.watfaq.com>'
    subject = u'加个蛋'
    to = 'Jiatai <liujiatai@gmail.com>'
    cc = 'Yuwei <akabyw@gmail.com>'
    text = text

    r = requests.post(api_host, auth=('api', token), data={
        'subject': subject,
        'from': sender,
        'to': to,
        'cc': cc,
        'text': text,
    })

    return r.status_code, r.content


if __name__ == '__main__':
    sched.start()
