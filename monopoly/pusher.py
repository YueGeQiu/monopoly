# -*- coding: utf-8 -*-

import datetime
import requests

SEND_KEY = ''
PUSH_BEAR_URL = 'https://pushbear.ftqq.com/sub'


def notify(text, desp):
    text = "{} - {}".format(datetime.date.today().strftime("%Y-%m-%d"), text)
    params = {
        'sendkey': SEND_KEY,
        'text': text,
        'desp': desp
    }
    print("about to notify subscribers")
    resp = requests.get(PUSH_BEAR_URL, params=params)
    print(resp.text)
    print(resp.json().get("data"))
