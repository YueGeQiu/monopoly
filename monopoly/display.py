# -*- coding: utf-8 -*-

from colorama import init, Fore, Back

EMOJI_UP = '📈'
EMOJI_DOWN = '📉'

# colorama init
# https://pypi.org/project/colorama/
init(autoreset=True)


def display_shell(name, open_price, close_price, current_price):
    percent = (current_price - close_price) / close_price * 100
    msg = Back.LIGHTWHITE_EX + "{:8s} 开盘价格: {:6.4f} 现价: {:6.4f} 涨跌幅: {:2.2f}%" \
        .format(name, open_price, current_price, percent)
    if percent < 0:
        msg = Fore.GREEN + EMOJI_DOWN + ' ' + msg
    else:
        msg = Fore.RED + EMOJI_UP + ' ' + msg
    print(msg)
