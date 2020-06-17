# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *


def init(context):
    # 订阅浦发银行, bar频率为一天
    subscribe(symbols='SHSE.600000', frequency='1d')


def on_bar(context, bars):
    # 打印当前获取的bar信息
    print(bars)


if __name__ == '__main__':
    run(strategy_id='16b4e735-5bd6-11ea-b738-0a0027000003',
        filename='data_drive.py',
        mode=MODE_BACKTEST,
        token='94f499de37e8705d51f18a53020f860751c97c76',
        backtest_start_time='2016-06-17 13:00:00',
        backtest_end_time='2017-08-21 15:00:00')
