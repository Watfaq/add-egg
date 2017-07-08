#encoding: utf-8
from apscheduler.schedulers.blocking import BlockingScheduler

import requests


sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=12)
def add_egg():
    print(send_mail(get_text(get_price())))


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

    sender = 'No Reply <no-reply@no-reply.alipay-inc.xyz>'
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
    sched.start()
