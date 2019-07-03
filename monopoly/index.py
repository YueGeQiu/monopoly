# -*- coding: utf-8 -*-

import tushare as ts
import traceback
import sys

from monopoly.display import display_shell


class Index(object):
    """
    Class for a type of Index, such as HS300
    """

    def __init__(self, code):
        self.code = code
        try:
            print("Init index of code: {}".format(code))
            data = ts.get_realtime_quotes(code)
            pandas_data = data.iloc[0]
            # for data format: http://tushare.org/trading.html
            self.name = pandas_data['name']
            self.open = float(pandas_data['open'])
            self.close = float(pandas_data['pre_close'])
            self.current = float(pandas_data['price'])
        except Exception as e:
            print("Init index {} failed: {}".format(code, e))
            traceback.print_exc(file=sys.stdout)
            raise RuntimeError
        # default display function
        self._display = display_shell

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, display_func):
        self._display = display_func

    def display_info(self):
        self.display(self.name, self.open, self.close, self.current)
