from gm.api import *

set_token('94f499de37e8705d51f18a53020f860751c97c76')

# def init(context):
#     # 指定数据窗口大小为50
#     subscribe(symbols='SHSE.600000', frequency='1d', count=50)
#
#
# def on_bar(context, bars):
#     # 打印频率为一天的浦发银行的50条最新bar的收盘价和bar开始时间
#     print(context.data(symbol='SHSE.600000', frequency='1d', count=50,
#                        fields='close,bob'))

history_data = history(symbol='SHSE.000300', frequency='1d', start_time='2010-07-28', end_time='2017-07-30', df=True)

print(history_data)
