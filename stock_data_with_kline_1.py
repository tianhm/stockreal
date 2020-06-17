#!/usr/bin/env python
# coding=utf-8
import pandas_datareader
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
from matplotlib.ticker import MultipleLocator

# 根据指定代码和时间范围，获取股票数据
code = '600895.ss'
stock = pandas_datareader.get_data_yahoo(code, '2019-01-01', '2019-03-31')
# 删除最后一行，因为get_data_yahoo会多取一天数据
stock.drop(stock.index[len(stock) - 1], inplace=True)
# 保存在本地
stock.to_csv('600895.csv')
df = pd.read_csv('600895.csv', encoding='gbk', index_col=0)
# 设置窗口大小
fig, ax = plt.subplots(figsize=(10, 8))
xmajorLocator = MultipleLocator(5)  # 将x轴主刻度设置为5的倍数
ax.xaxis.set_major_locator(xmajorLocator)
# 调用方法，绘制K线图
candlestick2_ochl(ax=ax,
                  opens=df["Open"].values, closes=df["Close"].values, highs=df["High"].values, lows=df["Low"].values,
                  width=0.75, colorup='red', colordown='green')
# 如下是绘制3种均线
df['Close'].rolling(window=3).mean().plot(color="red", label='3天均线')
df['Close'].rolling(window=5).mean().plot(color="blue", label='5天均线')
df['Close'].rolling(window=10).mean().plot(color="green", label='10天均线')
plt.legend(loc='best')  # 绘制图例
ax.grid(True)  # 带网格线
plt.title("600895张江高科的K线图")
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.setp(plt.gca().get_xticklabels(), rotation=30)
plt.show()
