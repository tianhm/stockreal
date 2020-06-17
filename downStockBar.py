#encoding:utf-8

import time
import tushare


def get_stock_list():
    # 获取正常上市交易的股票列表，主要用股票代码
    data = tushare.get_stock_basics()
    # 返回一个数据对象，索引列就是股票代码
    return data.index


def get_stock_hist_data(code, start='2010-01-01',
                        end=time.strftime('%Y-%m-%d', time.localtime())):
    # 获取股票历史数据
    # 调用tushare的get_hist_data()方法
    # 从中选取如下返回值：
    # date: 日期
    # code: 股票代码
    # open: 开盘价
    # high: 最高价
    # close: 收盘价
    # low: 最低价
    data = tushare.get_hist_data(code, start, end)
    # 存放数据的列表
    stock_list = []
    # 组合所需元素(日期-股票代码-开盘价-收盘价-最高价-最低价)
    temp = list(zip(data.index, [code for x in range(len(data.index))], data.open,
               data.close, data.high, data.low))
    for i in temp:
        stock_list.append(i)
    # 默认股票数据是最新日期在前的，想按日期生序排列，倒着返回
    return stock_list[::-1]

stocklist = get_stock_list()
# stocklist.sorted()
print(stocklist)
num = 0
for j in stocklist:
    stock = get_stock_hist_data(j)
    num += 1
    print(num, stock)
