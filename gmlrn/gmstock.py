# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals
from gm.api import *


def init(context):
    subscribe(symbols='SHSE.600000', frequency='1d')


def on_bar(context, bars):
    # 打印当前获取的bar信息
    bar = bars[0]
    # 执行策略逻辑操作
    print(bar)


if __name__ == '__main__':
    run(strategy_id='strategy_1', filename='gmstock.py', mode=MODE_BACKTEST, token='94f499de37e8705d51f18a53020f860751c97c76',
        backtest_start_time='2016-06-17 13:00:00', backtest_end_time='2017-08-21 15:00:00')