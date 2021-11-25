# import time
# import os
# from threading import Thread, current_thread
# from multiprocessing import Process, current_process


# COUNT = 200000000
# SLEEP = 10


# def io_bound(sec):

#     pid = os.getpid()
#     threadName = current_thread().name
#     processName = current_process().name

#     print(f"{pid} * {processName} * {threadName} \
#         ---> Start sleeping...")
#     time.sleep(sec)
#     print(f"{pid} * {processName} * {threadName} \
#         ---> Finished sleeping...")


# def cpu_bound(n):

#     pid = os.getpid()
#     threadName = current_thread().name
#     processName = current_process().name

#     print(f"{pid} * {processName} * {threadName} \
#         ---> Start counting...")

#     while n > 0:
#         n -= 1

#     print(f"{pid} * {processName} * {threadName} \
#         ---> Finished counting...")


# if __name__ == "__main__":
#     start = time.time()

#     # YOUR CODE SNIPPET HERE
#     # Code snippet for Part 1
#     # Code snippet for Part 2
#     # t1 = Thread(target = io_bound, args =(SLEEP, ))
#     # t2 = Thread(target = io_bound, args =(SLEEP, ))
#     # t1.start()
#     # t2.start()
#     # t1.join()
#     # t2.join()

#     # # Code snippet for Part 3
#     # cpu_bound(COUNT)
#     # cpu_bound(COUNT)

#     # # Code snippet for Part 4
#     # t1 = Thread(target = cpu_bound, args =(COUNT, ))
#     # t2 = Thread(target = cpu_bound, args =(COUNT, ))
#     # t1.start()
#     # t2.start()
#     # t1.join()
#     # t2.join()

#     # # Code snippet for Part 5
#     # p1 = Process(target = cpu_bound, args =(COUNT, ))
#     # p2 = Process(target = cpu_bound, args =(COUNT, ))
#     # p1.start()
#     # p2.start()
#     # p1.join()
#     # p2.join()

#     # Code snippet for Part 6
#     p1 = Process(target = io_bound, args =(SLEEP, ))
#     p2 = Process(target = io_bound, args =(SLEEP, ))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
#     end = time.time()
#     print('Time taken in seconds -', end - start)


# from concurrent.futures import process
# import os,sys
# import time
# import multiprocessing as mp
# from multiprocessing import Process,current_process
# import threading as th
# from threading import Thread,current_thread
# import binance
# from binance import Client
# client=Client()


# num=client.get_all_tickers()
# def check_api_call(stopper):
#     new_process = current_process().name
#     while   True:
#         client.get_symbol_ticker(symbol="ETHUSDT")
#         if stopper==True:
#             break

# def check_compute(value):
#     new_process = current_process().name
#     change=num-value


# r,w=os.pipe()
# processid=os.fork()
# if processid:
#     os.close(w)
#     os.fdopen(r)
#     num=r.read()
#     p1=Process(target =check_compute,args =(num,))
#     p1.start()
#     p1.join()
#     os.exit(0)
# else:
#     os.close(r)
#     os.fdopen(w,"w")

#     p2=Process(target=check_api_call,args=(False,))
#     p2.start()
#     p2.join()
#     w.write(p2)
#     os.exit(0)


# #!/usr/bin/python

# import os, sys

# print("The child will write text to a pipe and ")
# print("the parent will read the text written by child..."

# # file descriptors r, w for reading and writing
# r, w = os.pipe()

# processid = os.fork()
# if processid:
#    # This is the parent process
#    # Closes file descriptor w
#    os.close(w)
#    r = os.fdopen(r)
#    print("Parent reading")
#    str = r.read()
#    print("text =", str)
#    sys.exit(0)
# else:
#    # This is the child process
#    os.close(r)
#    w = os.fdopen(w, 'w')
#    print("Child writing")
#    w.write("Text written by child...")
#    w.close()
#    print("Child closing")
#    sys.exit(0)


# from multiprocessing import Process, Pipe
# import binance
# client=binance.Client()
# def parentData(parent):
#     while True:
#         ''' This function sends the data for the child process '''
#         a=client.get_all_tickers()
#         parent.send(a)
#         parent.close()

# def childData(child):
#     while True:
#         ''' This function sends the data for the parent process '''
#         child.send("Got It")
#         child.close()

# if __name__ == '__main__':
#     parent, child = Pipe()              # Create Pipe
#     process1 = Process(target = parentData, args = (parent, ))      # Create a process for handling parent data
#     process2 = Process(target = childData, args = (child, ))        # Create a process for handling child data
#     process1.start()                    # Start the  parent process
#     process2.start()                    # Start the child process
#     print(parent.recv())                # Display data received from child (BYE)
#     print(child.recv())                 # Display data received from parent (HELLO)
#     process1.join()                     # Wait till the process completes its execution
#     process2.join()


# import os
# import binance
# import multiprocessing as mp
# from multiprocessing import Process
# import asyncio
# # process=mp.Process()
# client = binance.Client()
# first=client.get_all_tickers()
# def get_coin()->list:
#     all_coins=client.get_all_tickers()
#     return all_coins
# def processing():
#     diff=float(first[1]['price'])
#     return diff


# if __name__ == '__main__':
#     p1=Process(target=get_coin, args=())
#     p2=Process(target=processing,args=())
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()


# import asyncio
# import time
# from multiprocessing import Process,Pipe

# async def test_function(number,number1):
#     num=number**number1
#     number=num*num
#     await asyncio.sleep(4)
#     # print(number)

# def test_function1(number,number1,fu1):
#     num=number**number1
#     number=num**1000
#     fun1.send(num)

#     time.sleep(4)
#     fun1.send(number)

#     # print(number)
# async def runner():
#     task1=await asyncio.gather(test_function(192,129)
#     ,test_function(201,102))
#     # test_function1(192,129)
# def runner1(run1):
#     a=run1.recv()
#     print(a)


# if __name__ == '__main__':
#     fun1,run1=Pipe()
#     timein=time.time()
#     process1=Process(target=test_function1, args=(192,129,fun1))
#     process2=Process(target=runner1, args=(run1,))
#     # process2=Process(target=test_function1, args=(201,102))
#     process1.start()
#     process2.start()
#     process1.join()
#     process2.join()
#     print(time.time()-timein)

# # timein=time.time()
# # # asyncio.run(test_function(100,100))
# # # test_function1(192,129)
# # # asyncio.run(runner())

# # # asyncio.run(test_function(192,129))
# # # test_function1(192,129)


# # asyncio.run(test_function(192,129))
# # asyncio.run(test_function(201,102))

# # print(time.time()-timein)


# # from binance import AsyncClient, ThreadedClient, threaded_stream, ThreadedWebsocketManager, ThreadedDepthCacheManager
# import asyncio
# from multiprocessing import Process, Pipe
# import time
# import binance
# client = binance.Client()
# present = client.get_all_tickers()
# def prices()->list:
#     return client.get_all_tickers()

# def check_price():
#     for j in range(1,11):
#         a=prices()
#         for i in range(len(a)):
#             start=float(present[i]['price'])
#             now=float(a[i]['price'])
#         print(j)


# def prices(send1):
#     for i in range(1, 100):
#         send1.send(client.get_all_tickers())


# def check_price(recieve):
#     for j in range(1, 100):
#         a = recieve.recv()
#         for i in range(len(a)):
#             start = float(present[i]['price'])
#             now = float(a[i]['price'])

#         print(j)

# print(j)
# if __name__ == '__main__':
#     time_start=time.time()
#     send1,recieve=Pipe()
#     p1=Process(target=prices,args=(send1,))
#     p2=Process(target=check_price,args=(recieve,))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
#     # check_price()
#     print(time.time()-time_start)
# time_start=time.time()
# check_price()
# print(time.time()-time_start)


# import binance
# import time
# import asyncio
# client=binance.AsyncClient()
# a=client.get_all_tickers()
# value=None
# async def check_price():
#     value= client.get_all_tickers()

# async def check(value):
#     task=asyncio.futures(check_price,check_price)
#     await check_price()
#     for i in range(len(a)):
#         b=(float(a[i]['price'])-float(value[i]['price']))*100/float(a[i]['price'])
#         if b>1:
#             print(b[i]['price'])

# asyncio.run(check)


# import os
# import multiprocessing as mp
# import binance
# import time
# client = binance.Client()

# def send():
#     while True:
#         time.sleep(2)
#         print(a.get()[1]['price'])


# def sender(a):
#     while True:
#         time.sleep(2)
#         a.put(client.get_all_tickers())


# print(client.get_ticker(symbol="ETHUSDT"))
# if __name__ == '__main__':
#     a=mp.Queue()
#     p1=mp.Process(target=send, args=())
#     p1=mp.Process(target=send, args=())
#     p2=mp.Process(target=sender, args=(a,))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()


# a=(1,2,3,4,4)
# print(a)

# import datetime
# import pandas as pd
# time=datetime.datetime
# print(time.now())
# #create plot of symbols and price with matplotlib


# import requests
# import shutil

# urls = "https://data.binance.vision/data/spot/daily/aggTrades/1INCHBTC/1INCHBTC-aggTrades-2021-10-23.zip"

# data=requests.get(urls, stream=True)
# with open("test_file",'wb') as data_file:
#         shutil.copyfileobj(data.raw,data_file)


# from datetime import date, timedelta

# def daterange(start_date, end_date):
#     for n in range(int((end_date - start_date).days)):
#         yield start_date + timedelta(n)

# start_date = date(2013, 1, 1)
# end_date = date(2015, 6, 2)
# for single_date in daterange(start_date, end_date):
#     print(single_date)

# f=open("/home/puneeth/programmes/others/bot/tmp/botter/binance_data/extract_data/ETHBTC-aggTrades-2021-09-01.csv","r")
# a=f.read()
# print(a[0])
# f.close()

# from sys import getsizeof
# import pandas as pd
# df=pd.read_csv("/home/puneeth/programmes/others/bot/tmp/botter/binance_data/extract_data/ETHBTC-aggTrades-2021-09-01.csv",nrows=4,header=None,skiprows=0)
# print(getsizeof(df))


# import os
# s=os.listdir()
# print(s)

# with open("binance_data/extract_data/ETHBTC-aggTrades-2021-09-01.csv","r") as f:
#         print(f.readlines())


# import pandas as pd
# # df=pd.DataFrame()
# import time

# def helper(num):
#         print("help",num)
#         time.sleep(10)
# import multiprocessing as mp
# main=[]
# for process in range(10):
#         main.append(mp.Process(target=helper, args=(process,)))
#         main[process].start()
# for process in range(10):
#         main[process].join()


# all_differences = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07,
#                    0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


# def process_args(all_differences):
#     print("""
#     Process 1   0.00 - 0.01     {}
#     Process 2   0.01 - 0.02     {}
#     Process 3   0.02 - 0.03     {}
#     Process 4   0.03 - 0.04     {}
#     Process 5   0.04 - 0.05     {}
#     Process 6   0.05 - 0.06     {}
#     Process 7   0.06 - 0.07     {}
#     Process 8   0.07 - 0.08     {}
#     Process 9   0.08 - 0.09     {}
#     Process 10  0.09 - 0.10     {}
#     Process 11  0.1 - 0.02      {}
#     Process 12  0.2 - 0.03      {}
#     Process 13  0.3 - 0.04      {}
#     Process 14  0.4 - 0.05      {}
#     Process 15  0.5 - 0.06      {}
#     Process 16  0.6 - 0.07      {}
#     Process 17  0.7 - 0.08      {}
#     Process 18  0.8 - 0.09      {}
#     Process 19  0.9 - 0.10      {}
#     """.format())
# process_args(all_differences)


# def process_args(all_differences):
#         print("All processes list with numbers")
#         print("""
#         Process 1   0.00 - 0.01
#         Process 2   0.01 - 0.02
#         Process 3   0.02 - 0.03
#         Process 4   0.03 - 0.04
#         Process 5   0.04 - 0.05
#         Process 6   0.05 - 0.06
#         Process 7   0.06 - 0.07
#         Process 8   0.07 - 0.08
#         Process 9   0.08 - 0.09
#         Process 10  0.09 - 0.10
#         Process 11  0.1 - 0.02
#         Process 12  0.2 - 0.03
#         Process 13  0.3 - 0.04
#         Process 14  0.4 - 0.05
#         Process 15  0.5 - 0.06
#         Process 16  0.6 - 0.07
#         Process 17  0.7 - 0.08
#         Process 18  0.8 - 0.09
#         Process 19  0.9 - 0.10
#         """)
# process_args(all_differences)


# a=[1,2,3,4,5,5]
# leg=len(a)
# a.append("1")
# print(a[leg:])

# import pandas as pd
# from matplotlib import pyplot as plt
# import sqlite3
# conn = sqlite3.connect("data.db")
# df=pd.read_csv("binance_data/extract_data/ETHUSDT-trades-2021-10-20.csv",header=None)
# print(df[4].head(10))
# df[4]=pd.to_datetime(df[4],unit='ms')
# df=pd.DataFrame(df)
# df.to_sql('check',conn)
# y=df[1]
# plt.plot(x,y)
# plt.show()
# print(x)

# import pandas as pd
# # dictionary={"hi":[1],"lo":[2],"me":[3]}
# # df=pd.DataFrame.from_dict(dictionary)
# # print(df)
# # dictionary["hi"].append(2)
# # dictionary["lo"].append(3)
# # dictionary["me"].append(4)
# # df=pd.DataFrame.from_dict(dictionary)
# df=pd.DataFrame([1,2,3,4,5],[1,2,3,4,6])
# print(df)
# df.append([1,2,3,4,0])

# print(df)


# import pandas as pd
# dictionary={"hi":[1,2,3], "lo":[1,2,4],"me":[1,2,7]}
# df=pd.DataFrame(dictionary)
# print(df)
# df.loc[len(df.index)]=[1,2,5]
# print(df)

# from datetime import datetime
# import time
# date_is=640362246
# date_is=datetime.fromtimestamp(date_is)
# print(date_is)
# date_is=datetime.utcfromtimestamp(date_is)

# print(date_is.strftime("%Y-%m-%d %H:%M:%S.%f+00:00 (UTC)"))
# def unixtime_time(number):
#     return datetime.fromtimestamp(number)
# print(unixtime_time(int(1634688000047/1000)))
# import sqlite3
# conn = sqlite3.connect('data.db')
# cur=conn.cursor()
# cur.execute("""
#         select strftime('%s', 'now');
# """)
# print(datetime.timestamp(datetime.now()))

# import logging
# from loguru import logger
# logging.basicConfig(level=logging.DEBUG,format="%(asctime)s: %(levelname)s: %(message)s")
# logging.debug("starting loop forever")
# logger.debug("log")
# """hike"""

# a=input("Type of signals getting : ")
# assert a=="live" or "historical"
# print(a)

# a=[]
# print(len(a))

# import os
# print(os.listdir("../"))

# val="https://data.binance.vision/data/spot/daily/aggTrades/SCRTBUSD/SCRTBUSD-aggTrades-2021-10-23.zip"
# import re
# print(re.findall("([A-Z]*-[a-zA-Z]*[-0-9]*)",val))

# d={1:2,3:4,5:7}
# for keys in d.keys():
#         print(keys," : ",d[keys])

# import os
# from loguru import logger
# def checks():
#     if os.path.isdir("binance_data"):
#         if os.path.isdir("binance_data/extract_data"):
#             logger.debug("Data Dirs exist")
#             print("********************************")
#             logger.debug("Continuing...")
#         else:
#             logger.debug("extract_data directory not found")
#             print("********************************")
#             logger.debug("creating extract_data directory in binance_data folder")
#             os.mkdir("binance_data/extract_data")
#             os.chdir("../")
#             logger.debug("Done")
#     else:
#         logger.debug("binance_data directory not found")
#         print("********************************")
#         logger.debug("Creating binance_data directory in root directory")
#         os.mkdir("binance_data/extract_data")
#         logger.debug("Creating extract_data directory in binance_data")
# checks()

# import  json
# def defaults_config(filename):
#     with open(filename, 'r') as config:
#         config_json=json.load(config)
#         return config_json['inputs']
# print(defaults_config("config.json"))


# #create connection to oracle database
# import cx_Oracle
# import sys
# def connect(user, password, dsn):
#     try:
#         return cx_Oracle.connect(user, password, dsn)
#     except cx_Oracle.DatabaseError as e:
#         (error, ) = e.args
#         print('Oracle-Error-Code:', error.code)
#         print('Oracle-Error-Message:', error.message)
#         sys.exit(1)
# connection=connect('system', 'oracle', 'localhost:49161/xe')
# cursor=connection.cursor()
# #insert into table 'it'
# cursor.execute("insert into it values(1)")
# print(cursor.fetchall())
# connection.commit()
# cursor.close()


# from data_loader import data_load
# data_load.parameters_handler()

# import json
# dictionary_1={1:2,3:4,5:7}
# dictionary_1=json.dumps(dictionary_1,indent=4)
# with open('example.json','w+') as dictionary_is:
#         dictionary_is.write(json.dumps(dictionary_1))

# Python program to write JSON
# to a file


# import json

# # Data to be written
# dictionary ={
# 	"name" : "sathiyajith",
# 	"rollno" : 56,
# 	"cgpa" : 8.6,
# 	"phonenumber" : "9976770500"
# }

# # Serializing json
# json_object = json.dumps(dictionary, indent = 4)

# # Writing to sample.json
# with open("example.json", "w") as outfile:
# # 	outfile.write(json_object)
# from binance_data_handler import binance_data
# import time


# class example(binance_data):
#     def __init__(self):
#         self.from_date = "20201120"
#         self.to_date = "20211229"
#         self.freq = 1

#     def calculate(self):
#         dates_list = {}
#         each = []
#         j = 0
#         k = 0
#         for dates in self.daterange():

#             k += 1
#             timestamp_is = int(time.mktime(dates.timetuple())*1000)
#             each.append(timestamp_is)
#             if k == self.freq:
#                 k = 0
#                 j += 1
#                 dates_list[j] = each
#                 each = []
#                 continue
#         return dates_list


# example1 = example()
# dates = example1.calculate()
# for date in dates.keys():
#     for each in dates[date]:
#         print("{} - {}".format(date, each))

# def checker(x,y,z):
#     a=input("a is : ")
#     print(a)
# import multiprocessing as mp
# if __name__ == "__main__":
#     checker_processes = []
       
#     tmp = 0
#     for process in range(10):
        
#             checker_processes.append(mp.Process(target=checker, args=(
#                 1, 10, 1)))
#             checker_processes[tmp].start()
#             tmp += 1

#     for process in range(10):
#         checker_processes[process].join()

