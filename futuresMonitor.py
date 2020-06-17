import pyttsx3
from pytdx.exhq import TdxExHq_API
from pytdx.exhq import TDXParams
from time import sleep
from playsound import playsound
from datetime import datetime
import pandas as pd
import numpy as np

from loguru import logger as mylog
from stockConstants import *

from function import get_k_line_column

from myfunction import HLV, HHV, LLV, MID, cross, CROSS, crossup, crossdown
from wavefunc21 import *

from stocks import stocks, stockdict
from tqsdk.ta import RSI

api = TdxExHq_API()

ttsengine = pyttsx3.init()
mylog.add("stock_trading_{time}.log", encoding='utf-8')

# ttsengine.say('我现在开始工作了。')
# ttsengine.runAndWait()

# from tdxdata.tdx_future_data import IP_LIST


IP_LIST = [{'ip': '112.74.214.43', 'port': 7727},
           {'ip': '59.175.238.38', 'port': 7727},
           {'ip': '124.74.236.94', 'port': 7721},
           {'ip': '218.80.248.229', 'port': 7721},
           {'ip': '124.74.236.94', 'port': 7721},
           {'ip': '58.246.109.27', 'port': 7721}
           ]


def ping(ip, port=7709):
    """
    ping行情服务器
    :param ip:
    :param port:
    :param type_:
    :return:
    """
    apix = TdxExHq_API()
    __time1 = datetime.now()
    try:
        with apix.connect(ip, port):
            if apix.get_instrument_count() > 10000:
                _timestamp = datetime.now() - __time1
                # self.strategy.writeCtaLog('服务器{}:{},耗时:{}'.format(ip, port, _timestamp))
                return _timestamp
            else:
                # self.strategy.writeCtaLog(u'该服务器IP {}无响应'.format(ip))
                return timedelta(9, 9, 0)
    except:
        # self.strategy.writeCtaError(u'tdx ping服务器，异常的响应{}'.format(ip))
        pass
        return timedelta(9, 9, 0)


# ----------------------------------------------------------------------
def select_best_ip():
    """
    选择行情服务器
    :return:
    """
    # self.strategy.writeCtaLog(u'选择通达信行情服务器')

    data_future = [ping(x['ip'], x['port']) for x in IP_LIST]

    best_future_ip = IP_LIST[data_future.index(min(data_future))]

    # self.strategy.writeCtaLog(u'选取 {}:{}'.format(best_future_ip['ip'], best_future_ip['port']))
    # print(u'选取 {}:{}'.format(best_future_ip['ip'], best_future_ip['port']))
    return best_future_ip



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
            mylog.info([stock, stockname, '发出交易信号', signal])
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
    rsi = RSI(bars, 6).rsi
    rsi = rsi.tolist()
    # rsiup = crossup(rsi, 20)
    # rsidown = crossdown(rsi, 80)

    (lastsig, sigall) = gen_rsi_signals(rsi, bars)

    print('---------------------R S I------------------------')
    print('当前时间:', bars.iloc[-1].datetime, 'K线数量:', len(bars), '信号数:', len(lastsig), '平均信号周期:', int(len(bars) / len(lastsig)))
    print('最近的信号:', lastsig[-1], sigall[-20:])
    print('K线周期:', interval, 'K线数量:', len(bars), '信号数:', len(lastsig), '平均信号周期:', int(len(bars) / len(lastsig)))
    print('信号价格:', lastsig[-1][2], '当前价:', bars.iloc[-1].close)
    print('最后k线:', bars.iloc[-1].datetime, '收盘价:', bars.iloc[-1].close)
    print('--------------------------------------------------')
    signal = sigall[-1]
    if signal == 'bpk' or signal == 'spk':
        signal = '买入' if signal == 'bpk' else '卖出'
        mylog.info([stock, stockname, '发出交易信号', signal])
        ttsengine.say(strategy + stockname + '发出'+signal+'信号')
        ttsengine.runAndWait()


def szStockProcess():
    szall = api.get_security_count(0)
    for step in range(0, szall, 1000):
        szsecs = api.get_security_list(0, step)
        # 处理深圳市场的标的
        for sec in szsecs:
            # print(sec)
            if sec['code'].startswith(('000', '300')):
                stock = sec['code']
                stockname = sec['name']
                print(sec['code'], sec['name'])

                market_code = 1 if str(stock)[0] == '6' else 0
                # data = api.get_security_bars(M15, market_code, stock, 0, 800)
                data = api.get_security_bars(H1, market_code, stock, 0, 300)
                datapd = api.to_df(data)

                if len(datapd) == 0:
                    print(stock, stockname)
                    sleep(5)
                else:
                    wave_info_display(datapd, stock, stockname)
                # wave_info_display(datapd, stock, stockname)

                # dingdang(data, stock, stockname)


def shStockProcess():
    # 处理上海市场的标的
    shall = api.get_security_count(1)
    for step in range(0, shall, 1000):
        shsecs = api.get_security_list(1, step)
        for sec in shsecs:
            if sec['code'].startswith('60') or sec['code'].startswith('68'):
                stock = sec['code']
                stockname = sec['name']

                print(sec['code'], sec['name'])
                market_code = 1 if str(stock)[0] == '6' else 0
                # data = api.get_security_bars(M15, market_code, stock, 0, 800)
                data = api.get_security_bars(DAY, market_code, stock, 0, 300)
                datapd = api.to_df(data)
                if len(datapd) == 0:
                    print(stock, stockname)
                    sleep(10)
                else:
                    wave_info_display(datapd, stock, stockname)
                # dingdang(data, stock, stockname )


if __name__ == '__main__':
    bsip = select_best_ip()
    ip = bsip['ip']
    port = int(bsip['port'])
    if api.connect(ip, port):
        num = api.get_instrument_count()
        all_contacts = sum([api.get_instrument_info((int(num / 500) - i) * 500, 500) for i in range(int(num / 500) + 1)], [])
        print(all_contacts)

        # 指数合约
        index_contracts = api.get_instrument_quote_list(42, 3, 0, 100)

        # 主力合约
        main_contracts = api.get_instrument_quote_list(60, 3, 0, 100)

        markets_code = api.get_markets()



        data = api.get_instrument_bars(TDXParams.KLINE_TYPE_DAILY, 8, "10000843", 0, 100)
        # 对所有合约处理，更新字典 指数合约-tdx市场，指数合约-交易所
        for tdx_contract in all_contacts:
            tdx_symbol = tdx_contract.get('code', None)
            if tdx_symbol is None:
                continue
            tdx_market_id = tdx_contract.get('market')
            if str(tdx_market_id) in Tdx_Vn_Exchange_Map:
                TdxFutureData.symbol_exchange_dict.update({tdx_symbol: Tdx_Vn_Exchange_Map.get(str(tdx_market_id))})
                TdxFutureData.symbol_market_dict.update({tdx_symbol: tdx_market_id})

        # data = api.get_k_data(stock, '2015-01-01', '2020-01-14')
        # shsecdict = {}
        # shall = api.get_security_count(1)
        # for step in range(0, shall, 1000):
        #     shsecs = api.get_security_list(1, step)
        #     for sec in shsecs:
        #         if sec['code'].startswith('68') or sec['code'].startswith('60'):
        #             stock = sec['code']
        #             stockname = sec['name']
        #             shsecdict[stock] = stockname
        #             print(sec['code'], sec['name'])
        #
        #
        # np.save('shsecsdict.npy', shsecdict)# Save
        #
        # # Load
        # shsecsdict = np.load('shsecsdict.npy', allow_pickle=True).item()
        # print(read_dictionary['hello']) # displays "world"
        # shsecdf = pd.DataFrame(shsecdict)
        # shsecsdf = api.to_df(shsecs)


        api.close()

        sleep(300)

        #
        # data = api.get_k_data(stock, '2017-07-03', '2019-07-10')
        # print(data)
        # data = api.to_df(api.get_security_bars(9, 0, stock, 0, 10))  # 返回DataFrame

        # print(data)
        #
        # print('sleep')

    '''
    
    def get_security_bars(self, category, market, code, start, count):
    
        category->
    
        K线种类
        0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线
        5 周K线
        6 月K线
        7 1分钟
        8 1分钟K线 9 日K线
        10 季K线
        11 年K线
    
        market -> 市场代码 0:深圳，1:上海
    
        stockcode -> 证券代码;
    
        start -> 指定的范围开始位置;
    
        count -> 用户要请求的 K 线数目，最大值为 800
    
    如：
    
    api.get_security_bars(9,0, '000001', 4, 3)
    
    '''