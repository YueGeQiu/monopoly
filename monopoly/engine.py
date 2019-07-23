# -*- coding: utf-8 -*-
import datetime
import os
import sys
from datetime import timedelta

import tushare as ts
from colorama import Fore

from monopoly.display import display_text
from monopoly.index import Index

VERSION = 'v1.6'

# 屁股带你赚大钱
TOKEN = os.getenv('MONOPOLY_TOKEN', '')
CODE_HS_300 = 'hs300'
CODE_SZ_50 = 'sz50'
MONEY_EACH_MONTH = 1000

HS300_HOLDING_POINT = 4000
HS300_SELLING_POINT = 4500
SZ50_HOLDING_POINT = 3000
SZ50_SELLING_POINT = 3500

PORTION_EACH_TIME = [0.1, 0.2, 0.4, 0.3]

if not TOKEN:
    print("ERROR: no token found")
    sys.exit(-1)

# set token
ts.set_token(TOKEN)


def calc_amount(total_amount: int, count):
    """

    :param total_amount: 每个月定投总额
    :param count: 阴线次数
    :return:
    """
    if count <= len(PORTION_EACH_TIME):
        return total_amount * PORTION_EACH_TIME[count - 1]
    else:
        return 0


def check_this_month(code=CODE_HS_300):
    """ Find count of "阴线" in this month

    :return: count
    """
    today = datetime.date.today()
    if today.day == 1:
        print('today is the first day of the month')
        yesterday = today
    else:
        yesterday = datetime.date.today() - timedelta(days=1)

    first_day_this_month = yesterday.replace(day=1)
    print("checking from {} to {}".format(first_day_this_month, yesterday))

    history_data = ts.get_hist_data(code,
                                    start=first_day_this_month.strftime("%Y-%m-%d"),
                                    end=yesterday.strftime("%Y-%m-%d"))
    # print(history_data)
    count = 0
    for index, row in history_data.iterrows():
        open_price = row['open']
        close_price = row['close']
        if float(close_price) < float(open_price):
            count += 1
    return count


def check_next_move(hs300_price, sz50_price):

    if hs300_price > HS300_SELLING_POINT or sz50_price > SZ50_SELLING_POINT:
        return "建议卖出"

    if hs300_price >= HS300_HOLDING_POINT or sz50_price >= SZ50_HOLDING_POINT:
        return "建议停止买入"

    return "屁股说：「观望观望。」"


def make_decision(hs300: Index, sz50: Index, amount):
    """ Make decision based on Index information

    :param hs300:
    :param sz50:
    :return:
    """
    decision = {
        'version': VERSION,
        hs300.name: hs300.display_info(),
        sz50.name: sz50.display_info()
    }

    message = ""
    if hs300.current < HS300_SELLING_POINT and hs300.current - hs300.open < 0:
        # check this month only history data
        count = check_this_month(CODE_HS_300) + 1
        message = "屁股说：「买特么的！」-> 这是本月第 {} 次阴线, 投 ￥ {} / ￥ {}, 屁股带你赚大钱".format(count,
                                                                              calc_amount(amount, count),
                                                                              amount)
    else:
        message = check_next_move(hs300.current, sz50.current)

    decision['屁股怎么说'] = message
    return decision


def check_for_app(amount=1000):
    try:
        hs300 = Index(CODE_HS_300)
        hs300.display = display_text
        sz50 = Index(CODE_SZ_50)
        sz50.display = display_text
        return make_decision(hs300, sz50, amount)
    except Exception as e:
        print("喊屁股修代码啦: {}".format(e))
