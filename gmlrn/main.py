# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *


def init(context):
    # 指定数据窗口大小为50
    subscribe(symbols='SHSE.600000', frequency='1d', count=50)


def on_bar(context, bars):
    # 打印频率为一天的浦发银行的50条最新bar的收盘价和bar开始时间
    print(context.data(symbol='SHSE.600000', frequency='1d', count=50,
                       fields='close,bob'))


if __name__ == '__main__':
    run(strategy_id='4440e18f-5bd6-11ea-b738-0a0027000003',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='94f499de37e8705d51f18a53020f860751c97c76',
        backtest_start_time='2016-06-17 13:00:00',
        backtest_end_time='2017-08-21 15:00:00')
