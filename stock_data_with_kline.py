#!/usr/bin/env python
# coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
from mplfinance import *

# 从文件里得到数据
df = pd.read_csv('002204', encoding='gbk')
print(df['open'].values)
# 设置图的位置
fig = plt.figure()
# ax = fig.subplot(111)
ax = plt.subplot(111)
# 调用方法，绘制K线图
candlestick2_ochl(ax, opens=df["open"].values, closes=df["close"].values, highs=df["high"].values, lows=df["low"].values,
                 width=0.75, colorup='red', colordown='green')

df['close'].rolling(window=3).mean().plot(color="red", label='3天均线')
df['close'].rolling(window=5).mean().plot(color="blue", label='5天均线')
df['close'].rolling(window=10).mean().plot(color="green", label='10天均线')
plt.legend(loc='best')  # 绘制图例
# 设置x轴的标签
plt.xticks(range(len(df.index.values)), df.index.values, rotation=30)
ax.grid(True)  # 带网格线
plt.title("600895张江高科的K线图")
plt.show()
