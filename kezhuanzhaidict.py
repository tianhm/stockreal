from easydict import EasyDict as edict
import numpy as np
from pytdx.hq import TdxHq_API
import pandas as pd

from loguru import logger as mylog
from stockConstants import *


kezhuanzhai = {}

def main():


    from pytdx.util.best_ip import select_best_ip
    stock_ip = select_best_ip('stock')
    print(stock_ip)
    api = TdxHq_API()

    if api.connect(stock_ip['ip'], stock_ip['port']):
        szall=api.get_security_count(0)
        shall=api.get_security_count(1)
        # szsecs = api.get_security_list(0, 0)
        # shsecs = api.get_security_list(1, 0)

        for step in range(0, shall, 1000):
            shsecs = api.get_security_list(1, step)
            for sec in shsecs:
                if sec['name'].endswith('转债'):
                    stock = sec['code']
                    stockname = sec['name']
                    kezhuanzhai[stockname] = [stock, 'sh']

                    print(sec['code'], sec['name'])

        for step in range(0, szall, 1000):
            szsecs = api.get_security_list(0, step)
            # 处理深圳市场的标的
            for sec in szsecs:
                # print(sec)
                if sec['name'].endswith('转债'):
                    stock = sec['code']
                    stockname = sec['name']
                    kezhuanzhai[stockname] = [stock,'sz']
                    print(sec['code'], sec['name'])

        np.save('kezhuanzhai.npy', kezhuanzhai)


# indexs = np.load('indexs.npy', allow_pickle=True)
# mains = np.load('mains.npy', allow_pickle=True)
# indexdict = edict(indexs.item())
# maindict = edict(mains.item())

kezhuanzhai = np.load('kezhuanzhai.npy', allow_pickle=True)

# print(kezhuanzhai)
kzz = edict(kezhuanzhai.item())


if __name__ == '__main__':
    # 合约调用例子, indexdict 返回的是快期的指数合约, maindict返回的是快期的主连合约.
    # main()
    kezhuanzhai = np.load('kezhuanzhai.npy', allow_pickle=True)

    print(kezhuanzhai)
    kzz = edict(kezhuanzhai.item())
    for k, v in kzz.items():
        if v[1] == 'sh':
            print('上海')
        if v[1] == 'sz':
            print('深圳')

