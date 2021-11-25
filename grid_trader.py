import os
import asyncio
from time import time, time_ns
import binance as exchange
import sqlite3 as database
import logging as log
# import colorama as colour
from colorama import Fore as colour
import json
from binance.enums import *

# Need to make use of the following code
# for frame in cycle(r'-\|/-\|/'):
#     print('\r', frame, sep='', end='', flush=True)
#     sleep(0.2)
client = exchange.Client()

# client.order_market_buy(symbol,quantity,)
# order=client.create_test_order(symbol='BNBBTC',
#     side=SIDE_SELL,
#     type=ORDER_TYPE_MARKET,
#     timeInForce=TIME_IN_FORCE_GTC,
#     quantity=0.1
#    )

class grid_trade:
    

    def get_coins(type_of):
        """request the coin to create the bot i.e grid bot"""
        if type_of == 0:
            execution = "/home/puneeth/programmes/others/bot/tmp/binance-pump-bot-main/python/detector/bin/python3 /home/puneeth/programmes/others/bot/tmp/binance-pump-bot-main/python/detect_telegram.py"
            return os.system(execution)
        elif type_of == 1:
            execution = "python3 -u /home/puneeth/programmes/others/bot/tmp/botter/detect.py"
            return os.system(execution)
        else:
            return "no coin input found"

    def get_values(file):
        """Take a  file and prints config file values and returns the dictionary"""
        file = json.load(file)
        values = file['configs'][0]
        for value in values:
            print(colour.LIGHTMAGENTA_EX+str(value) +
                  " : "+values[value]+"\n"+colour.RESET)
        
        return values

    def client_connect(config):
        """gets input of config and returns the client connection"""
        client = exchange.Client(config['api-key'], config['api-secret'])
        start = time()
        client.ping()
        print(colour.BLUE+"                                  PING time to api : {}".format(time()-start))
        return client

    # Binance API Helper Debug mode
    def debug_mode(client):
        """This function will print the realtime utc standard time of server and status"""
        # client.ping()
        time_res = client.get_server_time()
        print("                                        Server Time: {}".format(
            time_res["serverTime"]))

        status = client.get_system_status()
        print("                                          System Status: {}".format(
            status["msg"])+colour.RESET)

#need to do formating of the value of the amount to be placed for  limit orders only
    def market_orders(client, coin, value, type_of_order):
        
        """parameters :
        client(binance client)
        coin(coin name)
        value(amount to spend)
        type_of_order(order side buy or sell)               
        This function will send the market orders to the binance server depending on the type_of_order(buy or sell) , coin and value"""
        if type_of_order == "buy":
            market_order = client.order_market_buy(
                symbol=coin,
                quantity=value)
            return market_order
        elif type_of_order == "sell":
            market_order = client.order_market_sell(
                symbol=coin, quantity=value)
            return market_order
        else:
            print(
                colour.RED+"  ---------------------------------------------------------------")
            print(
                colour.RED+" | check the type_of_order you passed it in neither buy nor sell |"+colour.RESET)
            print(
                colour.RED+"  ---------------------------------------------------------------"+colour.RESET)
            return exit(1)

    def limit_orders(client, coin, value, type_of_order, which_price):
        """This function will send the limit orders to the binance server depending on the type_of_order(buy or sell) , coin , value
        and price at which order should be placed"""

        if type_of_order == "buy":
            limit_order = client.order_limit_buy(
                symbol=coin,
                quantity=value,
                price=which_price)
            return limit_order
        elif type_of_order == "sell":
            limit_order = client.order_limit_sell(
                symbol=coin,
                quantity=value, 
                price=which_price)
            return limit_order
        else:
            print(
                colour.RED+"  ---------------------------------------------------------------")
            print(
                colour.RED+" | check the type_of_order you passed it in neither buy nor sell |"+colour.RESET)
            print(
                colour.RED+"  ---------------------------------------------------------------"+colour.RESET)
            return exit(1)
    
    def cancel_orders(coin,id):
        open_orders=client.get_open_orders(symbol=coin)
        if id in open_orders:
            client.cancel_order(id)
            return 
        else:
            print("request for cancel failed order is filled !")






    def get_values_monitor(coin,id):
        """This function plays a key role in this strategy
        It monitors the market of the input coin and sends signals to the 
        buy sell order creator and stop loss function
        grid level manager to adjust
        the grid levels"""
        # client.get_avg_price(coin)
        # all_open=client.get_open_orders(symbol=coin)
        # all_are=client.get_all_orders
        # for open_orders in all_open:
        #     if open_orders["orderId"]==id:
        #         pass
        all_are=client.get_all_orders(symbol=coin)
        for orders in all_are:
            if orders["status"]=="FILLED":
                return orders

        




def main():
    print("================================")
    print(colour.YELLOW+"Starting grid_bot"+colour.RESET)
    print("================================")

    print(colour.GREEN+"getting values from configuration"+colour.RESET)
    values = {}
    with open("config.json") as file:
        values = grid_trade.get_values(file)
    print(colour.GREEN+"            ================================connecting to server===================================="+colour.RESET)
    client = grid_trade.client_connect(values)
    grid_trade.debug_mode(client)
    print(colour.GREEN+"For detect_telegram use 0 for detect_custom use 1 ")

    print(colour.LIGHTCYAN_EX+"checking market of the pair {}/{}".format(1,
          values["quote"])+colour.RESET)

    # print(colors.BOLD+colors.pretty_output.write('BOLD'+"checking market of the pair {}/{}".format(grid_trade.get_values(1)),values["quote"]))
    # print(client.get_all_tickers())
    # print(colour.RESET)


# main()
# print(grid_trade.get_coins(0))
# grid_trade.market_orders("client","btcUSDT",10,"none")
