from tafunc import *

import pyttsx3
from pytdx.hq import TdxHq_API
from time import sleep
from playsound import playsound
import pprint
from stockConstants import *
# from function import get_k_line_column
# from myfunction import HLV, HHV, LLV, MID, cross, CROSS
from stocks import stocks, stockdict

from datetime import datetime
from stocks import stocks, stockdict


# 获取当前日期
datenow = str(datetime.now().date())

ttsengine = pyttsx3.init()

ttsengine.say('小伟股票系统现在开始工作了。')
ttsengine.runAndWait()
api = TdxHq_API()

def between(s,a,b):
    if a<s and s<b:
        return True
    else:
        return False


with api.connect('119.147.212.81', 7709):
    while True:
        # data = api.get_k_data(stock, '2017-07-03', datenow)

        for stock in stocks:
            print('正在处理', stock, stockdict[stock])
            data = api.get_k_data(stock, '2017-07-03', datenow)
            data.dropna()

            # pprint.pprint(data)
            O = data.open
            # pprint.pprint(O)
            H = data.high
            L = data.low
            C = data.close
            V = data.amount

            # 计算小伟指标
            T = 30
            X1 = 5
            X2 = 5

            # N: = BARSLAST(DATE <> REF(DATE, 1)) + 1; 此句忽略
            #C1: = C / 3 + HHV(L, 3) / 3 + LLV(H, 3) / 3;
            C1 = C / 3 + hhv(L, 3) / 3 + llv(H, 3) / 3

            #CPX: MA(C1, 55), COLORYELLOW, LINETHICK2;
            CPX = ma(C1, 55)
            #X1: = MA(C1, 100);
            X1 = ma(C1, 100)
            #C3: = HHV(L, 3) / 3 + LLV(H, 3) / 3 + C / 3;
            C3 = hhv(L, 3) / 3 + llv(H, 3) / 3 + C / 3

            # ZQ: = BARSCOUNT(0);
            ZQ = len(data)
            # KL: = MAX(H - C, C - L), NODRAW;
            KL = max(H - C, C - L)
            # MAKL: = MA(KL, ZQ), NODRAW;
            MAKL = ma(KL, ZQ)
            # RH: = REF(HHV(C, T), 1);
            RH = ref(hhv(C, T), 1)
            # RL: = REF(LLV(C, T), 1);
            RL = ref(llv(C, T), 1)
            # BKX: = MIN(RL + X1 * MAKL, RH), COLORRED, LINETHICK2;
            BKX = min(RL + X1 * MAKL, RH)
            # SKX: = MAX(RH - X2 * MAKL, RL), COLORGREEN, LINETHICK2;
            SKX = max(RH - X2 * MAKL, RL)
            # pprint.pprint(BKX)
            # pprint.pprint(SKX)
            # print(BKX[-1])
            # print(SKX[-1])
            # print(ref(C,1))
            # print()
            # 买入信号 DRAWICON(C3 > CPX  AND RANGE(BKX, REF(C, 1), C); AND; MA(V, 5) > MA(V, 10), L * 0.98, 7);
            if C3[-1] > CPX[-1] and between(BKX[-1], ref(C, 1)[-1], C[-1]) and ma(V, 5) > ma(V, 10):
                print('买入信号发出')

            # 卖出信号 DRAWICON(RANGE(SKX, C, REF(C, 1)), H * 1.03, 8);
            if between(SKX[-1], C[-1], ref(C, 1)[-1]):
                print('卖出信号发出')

        sleep(300)
            #
            # market_code = 1 if str(stock)[0] == '6' else 0
            #
            # data = api.get_security_bars(M15, market_code, stock, 0, 800)
            #
