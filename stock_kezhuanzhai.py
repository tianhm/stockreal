import pyttsx3
from pytdx.hq import TdxHq_API
from time import sleep
import time
from playsound import playsound
from datetime import datetime
import pandas as pd
import numpy as np
from kezhuanzhaidict import kzz
from stockConstants import *
from loguru import logger as mylog
from function import get_k_line_column
from myfunction import HLV, HHV, LLV, MID, cross, CROSS, crossup, crossdown
from wavefunc21 import *
from tqsdk.ta import RSI

api = TdxHq_API(heartbeat=True)

ttsengine = pyttsx3.init()
mylog.add("stock_trading_{time}.log", encoding='utf-8')

ttsengine = pyttsx3.init()
mylog.add("kezhuanzhai_trading_{time}.log", encoding='utf-8')

# ttsengine.say('我现在开始工作了。')
# ttsengine.runAndWait()
def PytdxToAwpBar(bars):
    if not bars:
        return None
    awpbars = []
    for bar in bars:
        bartmp = {}
        bartmp['date_time'] = bar['datetime']
        bartmp['open'] = bar['open']
        bartmp['high'] = bar['high']
        bartmp['low'] = bar['low']
        bartmp['close'] = bar['close']

        awpbars.append(bartmp)

    return awpbars

def dingdang(data, stock, stockname):
    strategy = '叮当三号'
    bars = {stock: PytdxToAwpBar(data)}

    # print(bars[stock])
    O = get_k_line_column(bars[stock], ohlc='open')
    H = get_k_line_column(bars[stock], ohlc='high')
    L = get_k_line_column(bars[stock], ohlc='low')
    C = get_k_line_column(bars[stock], ohlc='close')

    uperband = HHV(H, 23)
    lowerband = LLV(L, 23)
    dingdangline = MID(uperband, lowerband)
    signalList = cross(C, dingdangline)
    buysigdetail = CROSS(C, dingdangline)
    sellsigdetail = CROSS(dingdangline, C)



    try:
        knum = len(H)
        signalall = buysigdetail.count(True) * 2
        avsigp = int(knum / signalall)

        if buysigdetail[-1]:
            print(stockname, '发出买入信号。。。')
            ttsengine.say(strategy + stockname + '发出买入信号。')
            ttsengine.runAndWait()
            # playsound('2.wav')
            print(stock, '最近的买入信号:', avsigp, buysigdetail[(knum - avsigp):])
            # sleep(1)

            sleep(2)
        elif sellsigdetail[-1]:
            print(stockname, '发出卖出信号。。。')
            ttsengine.say(strategy + stockname + '发出卖出信号。')
            ttsengine.runAndWait()
            # playsound('Alarm04.wav')
            print(stock, '最近的卖出信号:', avsigp, sellsigdetail[(knum - avsigp):])
            # sleep(1)

            sleep(2)

        print('-' * 50)
    except:
        pass

    # print(buysigdetail.count(True))
    # print(sellsigdetail.count(True))
    # print(dingdangline[(knum - avsigp):])
    # print(C[(knum - avsigp):])

def wave_info_display(bars, stock, stockname):
    strategy = '波段策略'
    interval = 600
    # mylog.info('计算策略指标...')
    (k2, g) = get_WaveTrader(bars)
    (lastsig, sigall) = gen_wave_signals(k2, bars)
    # mylog.info('计算完成...')

    if len(lastsig) > 0:
        zcyl = ''
        if lastsig[-1][0] == 'spk':
            zcyl = '压力位:'
        elif lastsig[-1][0] == 'bpk':
            zcyl = '支撑位:'

        print('---------------------WAVE------------------------')
        print('当前时间:', bars.iloc[-1].datetime, 'K线数量:', len(bars), '信号数:', len(lastsig), '平均信号周期:', int(len(bars) / len(lastsig)))
        print('最近的信号:', lastsig[-1], sigall[-20:])
        print('K线周期:', interval, 'K线数量:', len(bars), '信号数:', len(lastsig), '平均信号周期:', int(len(bars) / len(lastsig)))
        print('信号价格:', lastsig[-1][2], '当前价:', bars.iloc[-1].close, zcyl, g[-1])
        print('最后k线:', bars.iloc[-1].datetime, '收盘价:', bars.iloc[-1].close)
        print('--------------------------------------------------')
        signal = sigall[-1]
        if signal == 'bpk' or signal == 'spk':
            signal = '买入' if signal == 'bpk' else '卖出'
            mylog.info([strategy, stock, stockname, '发出交易信号', signal])
            ttsengine.say(strategy + stockname + '发出'+signal+'信号')
            ttsengine.runAndWait()

def gen_rsi_signals(rsi, klines):
    lastsig = []
    sigall = []
    sigcount = 0

    if not rsi:
        return None
    else:

        for i in range(len(rsi)):

            if i == 0 and rsi[i] > 20:
                # lastsig.append(['bpk', time_to_str(klines.iloc[i].datetime), klines.iloc[i].close])
                lastsig.append(['bpk', klines.iloc[i].datetime, klines.iloc[i].close])
                sigall.append('bpk')
            if i == 0 and rsi[i] < 80:
                lastsig.append(['spk', klines.iloc[i].datetime, klines.iloc[i].close])
                sigall.append('spk')
            # else:
            #     pass

            if rsi[i] > 20 and rsi[i - 1] <= 20:
                lastsig.append(['bpk', klines.iloc[i].datetime, klines.iloc[i].close])
                sigall.append('bpk')
                sigcount = 0
            elif rsi[i] < 80 and rsi[i - 1] >= 80:
                lastsig.append(['spk', klines.iloc[i].datetime, klines.iloc[i].close])
                sigall.append('spk')
                sigcount = 0
            else:
                sigcount += 1
                sigall.append(sigcount)

    return lastsig, sigall


def rsi_info_display(bars, stock, stockname):
    strategy = 'RSI策略'
    interval = 900
    # print(bars.close)
    rsi = RSI(bars, 6).rsi
    rsi = rsi.tolist()
    # rsiup = crossup(rsi, 20)
    # rsidown = crossdown(rsi, 80)

    (lastsig, sigall) = gen_rsi_signals(rsi, bars)
    if len(lastsig) >0:
        average_signal_periods = int(len(bars) / len(lastsig))
        print('---------------------R S I------------------------')
        print('当前时间:', bars.iloc[-1].datetime, 'K线数量:', len(bars), '信号数:', len(lastsig), '平均信号周期:', average_signal_periods)
        print('最近的信号:', lastsig[-1], sigall[-20:])
        print('K线周期:', interval, 'K线数量:', len(bars), '信号数:', len(lastsig), '平均信号周期:', int(len(bars) / len(lastsig)))
        print('信号价格:', lastsig[-1][2], '当前价:', bars.iloc[-1].close)
        print('最后k线:', bars.iloc[-1].datetime, '收盘价:', bars.iloc[-1].close)
        print('--------------------------------------------------')
        signal = sigall[-1]
        if signal == 'bpk' or signal == 'spk':
            signal = '买入' if signal == 'bpk' else '卖出'
            mylog.info([strategy, stock, stockname, '发出交易信号', signal])
            ttsengine.say(strategy + stockname + '发出'+signal+'信号')
            ttsengine.runAndWait()
    else:
        print('本标的无交易信号...')

def szStockProcess(interval):
    # szall = api.get_security_count(0)
    for step in range(0, szall, 1000):
        szsecs = api.get_security_list(0, step)
        # 处理深圳市场的标的
        for sec in szsecs:
            # print(sec)
            if sec['name'].endswith('转债'):
                stock = sec['code']
                stockname = sec['name']
                kezhuanzhai.append([stock, stockname])
                print(sec['code'], sec['name'])

                market_code = 1 if str(stock)[0] == '6' else 0
                # data = api.get_security_bars(M15, market_code, stock, 0, 800)
                # data = api.get_security_bars(H1, market_code, stock, 0, 300)
                data = api.get_security_bars(interval, market_code, stock, 0, 300)
                datapd = api.to_df(data)

                if len(datapd) == 0:
                    print(stock, stockname)
                    sleep(0.5)
                else:
                    # wave_info_display(datapd, stock, stockname)
                    rsi_info_display(datapd, stock, stockname)
                    # dingdang(data, stock, stockname)


def shStockProcess(interval):
    # 处理上海市场的标的, 可转债
    # shall = api.get_security_count(1)
    for step in range(0, shall, 1000):
        shsecs = api.get_security_list(1, step)
        for sec in shsecs:
            if sec['name'].endswith('转债'):

                stock = sec['code']
                stockname = sec['name']
                kezhuanzhai.append([stock, stockname])


                print(sec['code'], sec['name'])
                market_code = 1 if str(stock)[0] == '6' else 0
                market_code = 1
                # data = api.get_security_bars(M15, market_code, stock, 0, 800)
                # data = api.get_security_bars(H1, market_code, stock, 0, 300)
                data = api.get_security_bars(interval, market_code, stock, 0, 300)
                datapd = api.to_df(data)
                if len(datapd) == 0:
                    print(stock, stockname, '无数据...')
                    sleep(1)
                else:
                    # wave_info_display(datapd, stock, stockname)
                    rsi_info_display(datapd, stock, stockname)
                    # dingdang(data, stock, stockname )


def kezhuanzhaiProcess(interval):
        for k, v in kzz.items():

            if v[1] == 'sz':  #深圳市场
                market_code = 0
            elif v[1] == 'sh':
                market_code = 1

            stock = v[0]
            stockname = k
            # data = api.get_security_bars(M15, market_code, stock, 0, 800)
            # data = api.get_security_bars(H1, market_code, stock, 0, 300)
            data = api.get_security_bars(interval, market_code, stock, 0, 300)
            datapd = api.to_df(data)
            if len(datapd) == 0:
                print(stock, stockname, '无数据...')
                sleep(1)
            else:
                # wave_info_display(datapd, stock, stockname)
                rsi_info_display(datapd, stock, stockname)
                # dingdang(data, stock, stockname )


#判断是否为工作日,工作日返回1，非工作日返回0
def workDay():
    workTime=['09:25:00', '15:30:00']
    dayOfWeek = datetime.now().weekday()
    #dayOfWeek = datetime.today().weekday()
    beginWork=datetime.now().strftime("%Y-%m-%d")+' '+workTime[0]
    endWork=datetime.now().strftime("%Y-%m-%d")+' '+workTime[1]
    beginWorkSeconds=time.time()-time.mktime(time.strptime(beginWork, '%Y-%m-%d %H:%M:%S'))
    endWorkSeconds=time.time()-time.mktime(time.strptime(endWork, '%Y-%m-%d %H:%M:%S'))
    if (int(dayOfWeek) in range(5)) and int(beginWorkSeconds)>0 and int(endWorkSeconds)<0:
        return 1
    else:
        return 0


if __name__ == '__main__':
    from pytdx.util.best_ip import select_best_ip

    stock_ip = select_best_ip('stock')
    print(stock_ip)
    # future_ip = select_best_ip('future')
    # print(future_ip)



    # if api.connect('119.147.212.81', 7709):
    if api.connect(stock_ip['ip'], stock_ip['port']):

        count = 0
        while True:
            kezhuanzhaiProcess(M15)
            if workDay():

                kezhuanzhaiProcess(M15)

                # szStockProcess(M15)
                # shStockProcess(M15)
                count += 1
                print(['全市场第:', count, '轮询结束.'])
                sleep(300)

            else:
                print('非交易时间, 休息2分钟...')
                sleep(300)
