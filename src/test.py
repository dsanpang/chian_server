import json
import math
import threading
import time
import inspect
import urllib.request
import configparser
import asyncpg
import asyncio
import ctypes
# import numpy as np
import io
import sys
import pymysql

from my_redis import MyRedis

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

from tronpy.keys import to_base58check_address

config = configparser.ConfigParser()
config.read('src/conf/config.ini')

# np.set_printoptions(suppress=True, threshold=np.nan)

mode = 'LOCAL'

rd = MyRedis(config[mode]['redis_address'], int(config[mode]['redis_port']), config[mode]['redis_password'])


def runBTC(n):
    while 1:
        try:
            BTC_address = json.loads(rd.get("our_address_BTC"))
            run([{"network":"BTC","lists":BTC_address}],n)
        except Exception as err:
            print(str(err))

        #休息1秒
        time.sleep(1)


def runETH(n):
    while 1:
        try:
            ETH_address = json.loads(rd.get("our_address_ETH"))
            run([{"network":"ETH","lists":ETH_address}],n)
        except Exception as err:
            print(str(err))

        #休息1秒
        time.sleep(1)


def runBNB(n):
    while 1:
        try:
            BNB_address = json.loads(rd.get("our_address_BNB"))
            run([{"network":"BNB","lists":BNB_address}],n)
        except Exception as err:
            print(str(err))

        #休息1秒
        time.sleep(1)


def runTRX(n):
    while 1:
        try:
            TRX_address = json.loads(rd.get("our_address_TRX"))
            run([{"network":"TRX","lists":TRX_address}],n)
        except Exception as err:
            print(str(err))

        #休息1秒
        time.sleep(1)
    
    
def runAll(n):
    while 1:
        try:
            run([{"network":"BTC","lists":json.loads(rd.get("our_address_BTC"))}]+
            [{"network":"ETH","lists":json.loads(rd.get("our_address_ETH"))}]+
            [{"network":"BNB","lists":json.loads(rd.get("our_address_BNB"))}]+
            [{"network":"TRX","lists":json.loads(rd.get("our_address_TRX"))}],n)
        except Exception as err:
            print(str(err))

        #休息1秒
        time.sleep(1)


def run(All_address,n):
    # 每一个网络分成n份执行
    print(All_address)
    for row in All_address:
        print(row)
        network = row["network"]
        new_lists = []
        if len(row["lists"]) >= thread_sum and thread_sum > 1:
            j = 0
            for _list in row["lists"]:
                if j%thread_sum == n-1:
                    new_lists.append(_list)
                j = j + 1
        else:
            new_lists = row["lists"]
        
        #去执行
        # print("thread "+str(n)+":"+json.dumps({"network":network,"lists":new_lists}))
        go({"network":network,"lists":new_lists})


def go(data):
    for _list in data["lists"]:
        try:
            url = "http://127.0.0.1/api/notice/balance?network="+ str(data["network"]).lower() +"&addr=" + str(_list).lower()
            print(url)
            response = urllib.request.urlopen(url,timeout=15)
            rt = response.read().decode('utf-8')
            print(rt)
        except Exception as err:
            print(str(err))
        
        
        
def thread_run_btc_asyncio(n):
    asyncio.run(runBTC(n))
        
        
def thread_run_eth_asyncio(n):
    asyncio.run(runETH(n))
        
        
def thread_run_bnb_asyncio(n):
    asyncio.run(runBNB(n))
        
        
def thread_run_trx_asyncio(n):
    asyncio.run(runTRX(n))
        
        
def thread_run_all_asyncio(n):
    asyncio.run(runAll(n))
    
    
# 开始运行
thread_sum = 1 #开的线程数,线程数会平分所有地址，有助于提高处理效率，但线程数跟cpu核数及当前资源可调配有关系，并不是越多就越好。
for i in range(thread_sum): #BTC
    webThread = threading.Thread(target=thread_run_btc_asyncio,args=(i+1,))
    webThread.start()
    
thread_sum = 2 #开的线程数,线程数会平分所有地址，有助于提高处理效率，但线程数跟cpu核数及当前资源可调配有关系，并不是越多就越好。
for i in range(thread_sum): #ETH
    webThread = threading.Thread(target=thread_run_eth_asyncio,args=(i+1,))
    webThread.start()
    
thread_sum = 2 #开的线程数,线程数会平分所有地址，有助于提高处理效率，但线程数跟cpu核数及当前资源可调配有关系，并不是越多就越好。
for i in range(thread_sum): #BNB
    webThread = threading.Thread(target=thread_run_bnb_asyncio,args=(i+1,))
    webThread.start()
    
thread_sum = 2 #开的线程数,线程数会平分所有地址，有助于提高处理效率，但线程数跟cpu核数及当前资源可调配有关系，并不是越多就越好。
for i in range(thread_sum): #TRX
    webThread = threading.Thread(target=thread_run_trx_asyncio,args=(i+1,))
    webThread.start()
    
# for i in range(thread_sum): #全部
#     webThread = threading.Thread(target=thread_run_all_asyncio,args=(i+1,))
#     webThread.start()
