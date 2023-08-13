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

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

from tronpy.keys import to_base58check_address

config = configparser.ConfigParser()
config.read('conf/config.ini')

# np.set_printoptions(suppress=True, threshold=np.nan)

mode = 'LOCAL'


## DB Stuffs
def fetch(query):
    connection = pymysql.connect( 
        user=config[mode]['db_user'], 
        password=config[mode]['db_password'], 
        port=int(config[mode]['db_port']), 
        host=config[mode]['db_host'], 
        db=config[mode]['db_name'],
        charset="utf8" 
    )
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def fetchrow(query):
    connection = pymysql.connect( 
        user=config[mode]['db_user'], 
        password=config[mode]['db_password'], 
        port=int(config[mode]['db_port']), 
        host=config[mode]['db_host'], 
        db=config[mode]['db_name'],
        charset="utf8" 
    )
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchone()
        

def execute(query):
    connection = pymysql.connect( 
        user=config[mode]['db_user'], 
        password=config[mode]['db_password'], 
        port=int(config[mode]['db_port']), 
        host=config[mode]['db_host'], 
        db=config[mode]['db_name'],
        charset="utf8" 
    )
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor    
    
    
def fun1():
    print("fun1")
        
    
def fun2(AllThreads):
    while 1:
        i = 1
        for allThread in AllThreads:
            print("allThread.getName="+str(allThread.getName()))
            if allThread.is_alive():
                print("threading "+str(i)+": alive")
            else:
                print("threading "+str(i)+": no alive")
            i = i + 1
        time.sleep(3)
        
        
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
    raise SystemError("PyThreadState_SetAsyncExc failed")
            

def test():
    while 1:
        try:
            connection = pymysql.connect( user=config[mode]['db_user'], password=config[mode]['db_password'], port=int(config[mode]['db_port']), host=config[mode]['db_host'], db=config[mode]['db_name'], charset="utf8" )
            CONN = connection.cursor()
            sql = "select address,network from user where network='trx' order by create_time desc" #倒序
            #sql = "select address,network from user where network='trx' order by create_time asc" #正序
            CONN.execute(sql)
            rows = CONN.fetchall()
            for row in rows:
                print(row)
                if row[0] is not None:
                    url = "http://127.0.0.1/api/notice/balance?network="+ str(row[1]).lower() +"&addr=" + str(row[0]).lower()
                    print(url)
                    response = urllib.request.urlopen(url,timeout=15)
                    rt = response.read().decode('utf-8')
                    print(rt.encode("utf-8").decode("latin1"))
                    time.sleep(1)
        except Exception as err:
            print(str(err))

    time.sleep(1*5*5)
        
    # AllThreads = []
    # for i in range(3):
    #     webThread2 = threading.Thread(target=fun1,args=(i+1,AllThreads,))
    #     webThread2.start()
    #     webThread2.setName('test'+str(i))
    #     AllThreads.append(webThread2)
        
    # webThread = threading.Thread(target=fun2,args=(AllThreads,))
    # webThread.start()
    
    
# print(to_base58check_address("418840E6C55B9ADA326D211D818C34A994AECED808"))
# print("0x71afd498d0000".find('2323'))
# print(2/math.pow(10,16))
# print(eval('1.23456789e+25'))
test()
