#encoding: utf-8
from apscheduler.schedulers.blocking import BlockingScheduler

import requests


sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=12)
def add_egg():
    print(send_mail(get_text(get_price())))


@sched.scheduled_job('calc_lost_money', 'interval', minutes=1, id='calc_lost_money')
def calc_lost_money():
    price = get_price()
    sell = price['sell']
    lost = _calc_lose_money(float(sell))

    print 'Current lost %s...' % lost

    if lost > 10000:
        send_mail('Lost > %s' % lost)

    if lost < -50000:
        send_mail('Win 5w!!!!!!!!')
        send_mail('Win 5w!!!!!!!!')
        send_mail('Win 5w!!!!!!!!')


def _calc_lose_money(x):
    return ((16.72 - x) / 16.72 + 0.0002) * 40000


def get_price():
    r = requests.get('https://yunbi.com/api/v2/tickers').json()
    eos = r['eoscny']
    return eos['ticker']


def get_text(price):
    return '''
Cool!

Eos Sumary:
    Buy: {buy}
    Sell: {sell},
    Low: {low},
    High: {high},
    Last: {last},
    Vol: {vol}

Add an egg for your lunch!

'''.format(**price)


def send_mail(text):
    api_host = 'https://api.mailgun.net/v3/no-reply.alipay-inc.xyz/messages'
    token = 'key-40f226b6bc5d1f8065adb7177bbe4056'

    sender = 'NoReply <no-reply@no-reply.alipay-inc.xyz>'
    subject = u'加个蛋'
    to = 'Jiatai <liujiatai@gmail.com>'
    cc = 'Yuwei <akabyw@gmail.com>'
    text = text

    r = requests.post(api_host, auth=('api', token), data={
        'from': sender,
        'to': to,
        'cc': cc,
        'text': text,
    })

    return r.status_code, r.content


if __name__ == '__main__':
    # sched.start()
    calc_lose_money()
