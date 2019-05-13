# -*- coding: utf-8 -*-
import datetime
import os
import sys
from datetime import timedelta

import tushare as ts
from colorama import init, Fore, Back

VERSION = 'v1.4'

# 屁股带你赚大钱
TOKEN = os.getenv('MONOPOLY_TOKEN')
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
# colorama init
# https://pypi.org/project/colorama/
init(autoreset=True)


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


def check_this_month():
    """ Find count of "阴线" in this month

    :return: count
    """
    yesterday = datetime.date.today() - timedelta(days=1)
    first_day_this_month = yesterday.replace(day=1)

    print("checking from {} to {}".format(first_day_this_month, yesterday))

    history_data = ts.get_hist_data(CODE_HS_300,
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
        print(Fore.RED + "建议卖出")
        return

    if hs300_price >= HS300_HOLDING_POINT or sz50_price >= SZ50_HOLDING_POINT:
        print(Fore.YELLOW + "建议停止买入")
        return
    print(Fore.MAGENTA + "屁股说：「观望观望。」")


def display(name, open_price, close_price, current_price):
    percent = (current_price - close_price) / close_price * 100
    msg = Back.LIGHTWHITE_EX + "{:8s} 开盘价格: {} 现价: {} 涨跌幅: {:2.2f}%".format(name, open_price, current_price, percent)
    if percent < 0:
        msg = Fore.GREEN + msg
    else:
        msg = Fore.RED + msg
    print(msg)


def make_decision():
    data = ts.get_realtime_quotes([CODE_HS_300, CODE_SZ_50])
    # print(data.head())
    try:
        # for data format: http://tushare.org/trading.html
        hs300_name = data.iloc[0, 0]
        open_price = float(data.iloc[0, 1])
        close_price = float(data.iloc[0, 2])
        current_price = float(data.iloc[0, 3])

        sz50_name = data.iloc[1, 0]
        sz50_open_price = float(data.iloc[1, 1])
        sz50_close_price = float(data.iloc[1, 2])
        sz50_current_price = float(data.iloc[1, 3])

        # print("{} 开盘价格: {} 现价: {}".format(hs300_name, open_price, current_price))
        # print("{} 现价: {}".format(sz50_name, sz50_current_price))
        display(hs300_name, open_price, close_price, current_price)
        display(sz50_name, sz50_open_price, sz50_close_price, sz50_current_price)

        if current_price < HS300_SELLING_POINT and current_price - open_price < 0:
            print(Fore.GREEN + "-> 屁股说：「买特么的！」")
            # check this month only history data
            count = check_this_month() + 1
            print(Fore.GREEN + "-> 这是本月第 {} 次阴线, 投 ￥ {} / ￥ {}, 屁股带你赚大钱".format(count,
                                                                                calc_amount(MONEY_EACH_MONTH, count),
                                                                                MONEY_EACH_MONTH))
        else:
            check_next_move(current_price, sz50_current_price)
    except Exception as e:
        print("喊屁股修代码啦: {}".format(e))


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        MONEY_EACH_MONTH = int(sys.argv[1])
    make_decision()
