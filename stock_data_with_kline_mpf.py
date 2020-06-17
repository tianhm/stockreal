#!/usr/bin/env python
# coding=utf-8
import pandas_datareader
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

code = '600895.ss'
# stock = pandas_datareader.get_data_yahoo(code, '2019-01-01', '2020-02-28')
# stock.to_csv(code)
stock = pd.read_csv(code, index_col=0, parse_dates=True)
stock.index.name = 'Date'
stock.shape

mpf.plot(stock, type='candle')
mpf.plot(stock, type='ohlc', mav=(5, 12, 30), volume = True)
