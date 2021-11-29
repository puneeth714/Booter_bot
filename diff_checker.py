import re
from datetime import datetime
import time
import sqlite3
import multiprocessing as mp
import json
import os
# import pandas as pd
try:
    import binance
except:
    os.system("pip3 install python-binance")
    try:
        import binance
    except:
        os.system("sudo pip3 install python-binance")
        import binance
# import logging
from loguru import logger
logger.remove()
# import data_loader as dl
# logging.basicConfig(level=logging.INFO)
# send, receive = mp.Pipe()
all_differences = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07,
                   0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
receive, send = mp.Pipe()
price = None
client = binance.Client()
start = None


def fee_get(custom) -> float:
    """get fee for using in creating signals

    Args:
        custom (float): fee in binance(maker and taker fee)

    Returns:
        maker (float): None
        taker (float): None
    """
    maker, taker = input(
        "Enter the fee for maker and taker in binance(maker,taker) : ")
    return float(maker), float(taker)


def checks():  # sourcery skip: extract-duplicate-method
    if os.path.isdir("binance_data"):
        if os.path.isdir("binance_data/extract_data"):
            logger.debug("Data Dirs exist")
            print("********************************")
            logger.debug("Continuing...")
        else:
            logger.debug("extract_data directory not found")
            print("********************************")
            logger.debug(
                "creating extract_data directory in binance_data folder")
            os.mkdir("binance_data/")
            os.mkdir("binance_data/extract_data")
            os.chdir("../")
            logger.debug("Done")
    else:
        logger.debug("binance_data directory not found")
        print("********************************")
        logger.debug("Creating binance_data directory in root directory")
        os.mkdir("binance_data")
        os.chdir("binance_data")
        logger.debug("Creating extract_data directory in binance_data")
        os.mkdir("extract_data")
        os.chdir("../")
        logger.debug("Done")


def unixtime_time(number: int) -> datetime:
    """converts unixtime_time to datetime format used for converting binance historical data timestamp to datetime format
    which is usually milliseconds timestamp

    Args:
        number ([int]): [unixtime_timestamp]

    Returns:
        datetime: [datetime format of unixtime_timestamp]
    """
    logger.debug("unixtime_time to time is {}".datetime.fromtimestamp(
        int(number/1000)).strftime("%Y-%m-%dT%H:%M:"))
    return datetime.fromtimestamp(int(number/1000))


@logger.catch
def checker(start: list, upper: float, lower: float) -> Exception:
    """calls diff() function every n seconds to get the  signals
    works different for different types of signals for live it gets
    data from binance api which is fed using changer function and in historical type data is extracted from 
    the queue created which feeds the data from changer functions

    Args:
        start (list): starting prices of all coins_filter
        upper (float): upper side parameter for passing to diff() function
        lower (float): lower side parameter for passing to diff() function
    """
    start_each_value = {}
    started = 0
    logger.debug("starting loop forever")
    logger.debug("Type of data set to {}".format(typeof))
    price=None
    while True:
        # loop runs forever
        price = price1.get()
        if price=="completed":
            commits.put("exit")
            commits.join()
            print("checker completed")
            break
        """pipe gets data from changer function"""

        # if price == "completed":
        #     price1.put("ok")
        #     logger.info(
        #         "received all values and processing is done\nExiting.....")
        #     print('Done checker')
        #     exit(0)
        # #logger.debug("got price {}".format(price))
        # else:
        tmp=None
        if typeof == "historical":
            # if price == "done":
            #     print("No signals")
            #     exit(0)
            time_type = int(price[1])
            price = [price[0]]
            if started == 0:
                logger.debug("got price {}".format(price))

                start = price
            elif list(start_each_value.keys())[0] != price[0]['symbol']:
                start = price
                start_each_value = {}
        elif typeof == "live":
            time.sleep(2)
            time_type = datetime.timestamp(datetime.now())
        for i in range(len(price)):
            """This for loop runs for all values in the queue if live all symbols in historical specific data"""
            if start_each_value == {} or typeof == "live":

                start_each_value[start[i]['symbol']] = [
                    start[i]["price"], None, None, None, None]
            # start_each_value.append(float(start[i]['price']))
            update_price = diff(
                float(price[i]['price']), float(start_each_value[price[i]['symbol']][0]), upper, lower, price[i]['symbol'], time_type)
            try:
                if update_price[0]:
                    # start_each_value[i] = price[i]['price']
                    if typeof == "live":
                        each_time_start = time.time()
                    tmp=start_each_value[price[i]['symbol']
                                     ][0]
                    start_each_value[price[i]['symbol']
                                     ][0] = price[i]['price']
                if update_price[1] == "sell":
                    start_each_value[price[i]['symbol']][2] = True
                    start_each_value[price[i]
                                        ['symbol']][4] = update_price[4]
                else:
                    start_each_value[price[i]['symbol']][1] = True
                    start_each_value[price[i]
                                        ['symbol']][3] = update_price[3]

                        # buy_sell_signals(update_price[1],price[i]['symbol'],upper,lower)
            except Exception:
                pass
                # print(Exception)
                # continue
            if start_each_value[price[i]['symbol']][1] == True and start_each_value[price[i]['symbol']][2] == True:
                """checks if the price of an instrument has changed in both directions i.e this condition become true when buy and sell signals are created by a
                    particular pair(Instrument)"""
                end_time_filled = None
                if typeof == "historical":
                    end_time_filled = int(
                        start_each_value[price[i]['symbol']][3]-start_each_value[price[i]['symbol']][4])/1000
                    if end_time_filled < 0:
                        end_time_filled = -1*end_time_filled
                elif typeof == "live":
                    end_time_filled = time.time()-each_time_start
                # print(price[i]['symbol'])
                # print("\n\n")
                logger.debug("buy and sell signals created for {} with upper {} and lower {} and time_taken {}".format(
                    price[i]['symbol'], upper, lower, end_time_filled))
                insert_into(symbol=price[i]['symbol'], upper=upper,
                            lower=lower, time_taken=end_time_filled, work='buy_sell',
                            present=float(price[i]['price']), side=update_price[1], to_check=update_price[2],
                            check_with=float(tmp), time_type=time_type)
                start_each_value[price[i]['symbol']][1] = None
                start_each_value[price[i]['symbol']][2] = None
                # buy_sell_signals(price[i]['symbol'],
                #                  upper, lower, end_time_filled)
        # if typeof == "historical":
        #     start_each_value[price[i]['symbol']
        #                              ][0] = price[i]['price']
        # b=start_each_value
        # print("b is ",b)
        started += 1


@logger.catch
def diff(present: float, check_with: float, lower: float, upper: float, symbol: str, time_type: int) -> list:
    """finds difference between present and check_with and creates signals and inserts the signals into the database

    Args:
        present (float): present value of the coin
        check_with (float): difference checking with this value
        lower (float): parameter lower bound
        upper (float): parameter upper bound
        symbol (str): symbol/market pair name
        time_type (int):used in using historical data for setting time of signals
    Returns:
        list: returns a list containing the signals status and type(buy or sell)
    """
    # if symbol=="LTCBTC":
    #     print("LTCBTC")
    #logger.debug("Entered diff")
    if float(present)-float(check_with) > 0:
        """check if price changed is positive or negative"""
        to_check = float(((present-check_with)*100/present)-0.15)
        # print("   1")
        if to_check > float(lower) and to_check < float(upper):
            """check if price changed is positive even removing the maker/taker fee for a given fee of 0.15 then create a sell signals"""

            signal1 = "sell"
            insert_into(present, check_with, to_check,
                        signal1, upper, lower, symbol, work="diff", time_taken=None, time_type=time_type)
            """write to the log file log.txt (default) can specify any name and appends the data each time"""
            logger.debug("{} created for pair {} from pice {} to price {} with difference {} at time {} ".format(
                signal1, symbol, present, check_with, to_check, time_type))
            write_file("log.txt", "present = {},check_with = {},to_check = {},signal1 = {},upper = {},lower = {}, symbol = {}\n".format(
                present, check_with, to_check, signal1, upper, lower, symbol))
            # if symbol == "LTCBTC":
            #     print("{} -> {},    {}   {}".format(to_check, signal1, upper, lower))
            return [True, 'sell', to_check, 0, time_type]
    else:
        to_check = float(((present-check_with)*100/present)+0.15)*-1
        if to_check > float(lower) and to_check < float(upper):
            """check if price changed is negative even removing the maker/taker fee for a given fee of 0.15 creates buy signals"""

            signal1 = "buy"
            """insert buy signals into table"""
            logger.debug("{} created for pair {} from pice {} to price {} with difference {} at time {} ".format(
                signal1, symbol, present, check_with, to_check, time_type))
            insert_into(present, check_with, to_check,
                        signal1, upper, lower, symbol, work="diff", time_taken=None, time_type=time_type)
            """write file based on this signals(log.txt default)"""
            write_file("log.txt", "present = {},check_with = {},to_check = {},signal1 = {},upper = {},lower = {}, symbol = {}\n".format(
                present, check_with, to_check, signal1, upper, lower, symbol, time_type))
            # print("{} -> {},    {}   {}".format(to_check, signal1, upper, lower))
            return [True, 'buy', to_check, time_type, 0]


@logger.catch
def insert_into(present: float, check_with: float, to_check: float, side: str, upper: float, lower: float, symbol: str, work: str, time_taken: float, time_type: int):
    """inserting into data.db sqlite commands

    Args:
        present (float): present value
        check_with (float): difference to be check_with
        to_check (float): difference
        side (str): buy or sell
        upper (float): parameter upper bound
        lower (float): parameter lower bound
        symbol (str): symbol name
        work (str): type of insertion
        time_taken (float): time taken for buy_sell_signals
    """
    # if typeof == "live":
    #     time_type = 'CURRENT_TIMESTAMP'
    # elif typeof == "historical":
    #     time_type = time_type
    if work == "diff":

        # a = """insert into parameter_{} values({},'{}',{},{},{},"{}");""".format(str(lower)[str(
        #     lower).index(".")+1:]+"_"+str(upper)[str(upper).index(".")+1:], time_type, symbol, present, check_with, to_check, side)
        """query that is going to be executed"""
        query = """insert into parameter values
        ({},'{}',{},{},{},"{}","{}","{}");""".format(time_type, symbol, present, check_with, to_check, side,
                                                     str(lower), str(upper))
        write_file("log.txt", """{},'{}',{},{},{},"{}","{}","{}";""".format(time_type, symbol, present, check_with, to_check, side,
                                                                            str(lower), str(upper)))

        # print("")

        # conn.execute(a)

        # conn.cursor().close()
        commits.put_nowait(query)

        # print(sqlite3.Cursor.fetchall(conn.execute("select * from parameter_01_02")))
        # print("Hi")
    elif work == "buy_sell":
        """insert into table the instrument info which created both buy and sell signals"""
        """This will be true when the work parameter of the function is set to "buy_sell"""

        """query that is going to be executed"""
        query = """insert into buy_sell_signals values({},{},{},{},'{}','{}','{}','{}')""".format(
            time_type, present, to_check, check_with, symbol, upper, lower, time_taken)

        """write file based on this signals(log.txt default)"""
        write_file("log.txt", """({},{},{},{},'{}','{}','{}','{}')""".format(
            time_type, present, to_check, check_with, symbol, upper, lower, time_taken))
        try:
            """Try to execute the query"""
            commits.put_nowait(query)
        except:
            """If exception occurred create a table and try again"""
            table_created = """create table if not exists buy_sell_signals (
                time integer,
                present float,
                to_check float,
                check_with float,
                symbol TEXT,
                upper float,
                lower float,
                time_taken float
                );"""
            conn.execute(table_created)
            conn.cursor().close()
            conn.execute(query)
            conn.cursor().close()


logger.catch()
def commiter():
    """execute the query in given connection of database"""
    query = commits.get()
    tmp = 0
    while True:
        if tmp != 0:
            try:
                query = commits.get_nowait()
                if query == "exit":
                    conn.close()
                    break
            except:
                commiter()
        else:
            tmp = 1
        try:
            conn.execute(query)
        except sqlite3.OperationalError:
            logger.error("sqlite3.OperationalError got")
            time.sleep(0.1)
            commiter()
        logger.debug("query {} executed".format(query))
        conn.commit()

        # conn.cursor().close()
        # logger.info('committed {}'.format(conn.fetchall()))
        # conn.cursor().close()
        """commit the transaction"""
    print("commiter completed")

@logger.catch
def create_table():
    """create tables for parameters
    """
    # for i in range(19):
    #     """create tables for each type of parameter"""
    #     set = str(all_differences[i])[str(all_differences[i]).index(
    #         ".")+1:]+"_"+str(all_differences[i+1])[str(all_differences[i+1]).index(".")+1:]
    #     conn.execute("""create TABLE parameter_{}(
    #     time_fetch NUMBER,
    #     coin VARCHAR,
    #     present FLOAT,
    #     check_with FLOAT,
    #     to_check FLOAT,
    #     signal CHAR
    # )

    #     """.format(set))
    try:
        """table for all types of parameters"""
        """Only this table is called by default"""
        conn.execute("""create table parameter(
            
                time_fetch Text,
                market_pair VARCHAR,
                present FLOAT,
                check_with FLOAT,
                to_check FLOAT,
                signal CHAR,
                lower CHAR,
                upper CHAR
            );
        """)
        table_created = """create table  buy_sell_signals (
                time integer,
                present float,
                to_check float,
                check_with float,
                market_pair TEXT,
                lower float,
                upper float,
                time_taken float
                );"""
        conn.execute(table_created)
        conn.commit()
        conn.cursor().close()

    except:
        logger.warning(
            "table {} already present \n continuing....".format('parameter'))
        # print(Exception)


@logger.catch
def delete_table():
    """delete tables not reusable for now"""
    # for i in range(19):
    """delete tables all tables of parameter_xx_xx conventions except parameter table"""
    #     """Not used by default any more"""
    #     set = str(all_differences[i])[str(all_differences[i]).index(
    #         ".")+1:]+"_"+str(all_differences[i+1])[str(all_differences[i+1]).index(".")+1:]
    #     conn.execute("""drop table parameter_{}""".format(set))
    """Deleting parameter tables"""
    conn.execute("""drop table parameter;""")
    try:
        """Deleting buy_sell_signals table"""
        conn.execute("""drop table buy_sell_signals;""")
    except:
        print(Exception)


@logger.catch
def changer(data: str, sender: mp.Queue):
    """fetches the price of all markets in binance for every specified seconds this value is send to checker function using queues
    or it can be used to get historical data from binance aggTrades or trades and use that data for creation of signals

    just set parameter data=live or historical (historic will ask for some other parameters or it can read parameters from historic.json file)

    Args:
        data (str): Sets type of data  fetching method to use
        sender (mp.Queue): used in historical data fetching for getting name('s) of files from data_loader file
    """

    # global price
    if data == "live":
        """If live data to be used wait for certain time and fetch data from binance and put data in queue to be send to checker function"""
        while True:
            # global price
            time.sleep(5)
            try:

                price = client.get_all_tickers()
            except:
                """Exception is raised when connection is not created with binance server"""
                print(Exception)
                print("Connection problem")
                exit(0)
            # print(price[11]['price']+"   1")
            price1.put_nowait(price)
    elif data == "historical":
        """If data fetching method set to historical data then get name of the file from data_loader using queue"""
        """open the file and read data (normally a csv file) line by line and send symbol name(Actually pair or 
        Instrument name) , price and timestamp to checker function using queues"""
        while True:
            filename = sender.get()
            print(filename)
            if filename == "done":
                break
            os.chdir("binance_data/extract_data")
            # with pd.read_csv(filename,"r") as f:
            it_is = re.search("[0-9A-Z]*", filename)
            with open(filename, 'r') as f:
                for line in f.readlines():
                    line = line.split(",")

                    send = {'symbol': filename[:it_is.span()[1]]}
                    send['price'] = line[1]
                    price1.put_nowait([send, line[4]])
                    # price1.unfinished_tasks
            os.chdir("../../")
            # sender.put("done")
        if filename=="done":

            sender.put("completed")
            if sender.empty() or not sender.empty():
                print("done")
                # mp.Process.terminate()
    else:
        """if typeof didn't match live or historical raise a problem and ask for entering data and call this function(changer) again until value matches any"""
        print("you have entered {} which is not live nor historical".format(data))
        print("Try again")
        print("If want to exit please enter ctrl+c to exit")
        data = input("enter the data collection type")
        changer(data, sender)
        # send.send(price)
        # print(price)

# def buy_sell_signals(symbol, upper, lower, time_taken):
#     query = """insert into buy_sell_signals({},{},{},{},{})""".format(
#         'CURRENT_TIMESTAMP', symbol, upper, lower, time_taken)
#     conn.execute(query)


@logger.catch
def connection_to_database(database: str) -> sqlite3.Connection:
    """connection to database

    Args:
        database (str): file name or file path(can be relative)

    Returns:
        sqlite3.Connection: connection object
    """
    try:
        connection = sqlite3.connect(database)
        logger.debug("connection to database established")
        # print("connection established")
        logger.debug(
            "returning connection to database object {}".format(connection))
        return connection
    except:
        # print("failed to connect to database")
        # print("Exiting...")
        logger.error("failed to connect to database")
        logger.error("Exiting...")
        exit()


@logger.catch
def check_database(log_level: int, keep_delete=None) -> None:
    """check database if exists check tables if exists ................

    Args:
        log_level (int): log level to output to console(stdout)
        keep_delete(int):To keep the tables(0) or delete the tables(1) and create the new tables 
    """
    if "data.db" in os.listdir():
        # print("data.db exists")
        # print("continuing to check tables ...")
        logger.info("data.db exists")
        logger.info("continuing to check tables ...")
        try:
            create_table()
        except:
            print("tables all ready exists")
            if keep_delete is None:
                keep_delete = input(
                    "Do you want to keep the tables(0) or delete the tables(1) and create the new tables ? \n")
            if keep_delete == '1':
                print("Deleting tables....")
                delete_table()
                print("done deleteting tables")
                print("Createing tables....")
                create_table()
                print("Done creating tables")
            print("continuing...")

    else:
        print("no data.db found")
        print("creating database file")
        os.open("data.db", os.O_CREATE, 0o644)
        create_table()


@logger.catch
def coins() -> list:
    """fetches all coins from exchange

    Returns:
        list: list of coins in api return order
    """
    array = []
    """usually needs start list fetched when importing diff_checker"""
    """but can also work if not provided by self collecting the data from binance"""
    try:
        for i in range(len(start)):
            array.append(start[i]['symbol'])
    except:
        try:
            from pairs import pairs_list
            return pairs_list
        except:
            import binance
            return binance.Client().get_all_tickers()
    return array


@logger.catch
def log_level(log_should_be=None) -> bool:
    # """Need to implement not used any where yet"""
    """specify the log level for all the process in the checker system

    Returns:
        int: log size
    """
    if log_should_be is None:
        log_should_be = input(
            "log level of the process : 1.DEBUG\n2.INFO\n3.WARNING\n4.ERROR\n5.CRITICAL\n")
    # Caution, may leak sensitive data in prod
    logger.add("out.log", backtrace=True, diagnose=True, level=log_should_be)
    logger.debug("log level set to {}".format(log_should_be))
    return True


@logger.catch
def write_file(file: str, data: str) -> bool:
    """write log to the file

    Args:
        data (str): string to write to the file

    Returns:
        bool: status of write operation True(Done)/False(Exception/Error)
    """
    try:
        with open(file, 'a+') as f:
            f.write(data)
        return True
    except IOError:
        return False


@logger.catch
def database_journal_model(conn: sqlite3.Connection, mode=None):
    """changes the database journal mode to the specified mode

    Args:
        mode (str): by default it is set to WAL mode
        conn (sqlite3.Connection): connection to the database
    """
    try:
        conn.execute("""PRAGMA journal_mode={};
        """.format(mode))
        logger.info("Database journal mode set to {}".format(mode))
        return True
    except:
        # print("Can't change journal mode")4
        logger.warning("Can't change journal mode")
        logger.error(FileNotFoundError)
        """warning"""
        return FileNotFoundError


@logger.catch
def type_of_signals(type_is=None) -> str:
    """gets the type of signals from user to use further in the program

    Returns:
        str: should be live or historical error otherwise and give another chance to try again
    """
    print("Enter the type of signals you want to use: live or historical")
    if type_is is None:
        type_is = input("Type of signals getting : ")
    if type_is in ["live", "historical"]:
        if type_is == "live":
            global price, client, start
            price = client.get_all_tickers()
            client = binance.Client()
            start = client.get_all_tickers()

        logger.info("type_is is set to {}".format(type_is))
        return type_is
    else:
        print("Your input didn't match any of the available choices {} or {}".format(
            "historical", "live"))
        print("Try again \n Or Press ctrl+C to exit")
        try:

            return type_of_signals()
        except KeyboardInterrupt:
            print("Press ctrl+")
            print("..........Exiting.......")
            exit("value error")


@logger.catch
def process_args(all_differences):
    print("All processes list with numbers")
    print("""
        Process 1   0.00 - 0.01     
        Process 2   0.01 - 0.02     
        Process 3   0.02 - 0.03     
        Process 4   0.03 - 0.04     
        Process 5   0.04 - 0.05     
        Process 6   0.05 - 0.06     
        Process 7   0.06 - 0.07     
        Process 8   0.07 - 0.08     
        Process 9   0.08 - 0.09     
        Process 10  0.09 - 0.10     
        Process 11  0.1 - 0.2      
        Process 12  0.2 - 0.3      
        Process 13  0.3 - 0.4      
        Process 14  0.4 - 0.5      
        Process 15  0.5 - 0.6      
        Process 16  0.6 - 0.7      
        Process 17  0.7 - 0.8      
        Process 18  0.8 - 0.9      
        Process 19  0.9 - 1.0      
        """)


@logger.catch
def process_type(processes_list_or_string=None):
    process_args(all_differences)
    if processes_list_or_string is None:
        processes_list_or_string = input(
            "Start all processes \n OR specific process(s) only \n Enter any integer for  processes \n or comma separated values for processes :\n Enter all for all processes : \n")
    length = 0
    if type(processes_list_or_string) == str and processes_list_or_string != 'all':
        if "," in processes_list_or_string:
            processes_list_or_string = processes_list_or_string.split(",")
            length = len(processes_list_or_string)
            for value in processes_list_or_string:
                if type(value) == str:
                    try:
                        processes_list_or_string.append(int(value))
                    except:
                        print(
                            "May have entered non-integer values try again \n Exiting...")
            logger.info("The process list is {}".format(
                processes_list_or_string[length:]))
            return processes_list_or_string[length:]
        else:
            try:
                processes_list_or_string = int(processes_list_or_string)
                logger.info("The process list is {}".format(
                    processes_list_or_string))
                return [processes_list_or_string]
            except Exception as e:
                print(
                    "May have entered non-integer values try again \n Exiting...")
                exit(e)
            # return [int(processes_list_or_string)]
    elif processes_list_or_string == "all":
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


@logger.catch
def keep_delete_files(file1: str, file2: str, value=None) -> bool:
    """Deletes the files specified by parameter 1 and parameter 2 and input from the user 
    using system call from python using os module

    Args:
        file1 (str): usually the database file
        file2 (str): usually the log file

    Returns:
        bool: return's the value of user input if successful and error/warning for any failure
    """
    print("Delete {} , {} files".format(file1, file2))
    print("If you want to delete all files      :   3\n")
    print("If you want to delete specific file  : \n        1 -> for {}\n        2-> for {}  : \n       ".format(file1, file2))
    print("If you Don't want to delete any file :   0 ")
    if value is None:
        value = int(input("----------"))
    if int(value) == 3:
        print("Deleting all files i.e {} and {} :\ .....".format(file1, file2))
        if os.path.isfile("{}".format(file1)) == True and os.path.isfile("{}".format(file2)) == True:
            os.system("rm {}".format(file1))
            os.system("rm {}".format(file2))
        elif os.path.isfile("{}".format(file1)) == True:
            print("{} file not present".format(file2))
            print("Skiping Deleteing {} file and deleting {} ...".format(file2, file1))
            os.system("rm {}".format(file1))
            return 1
        elif os.path.isfile("{}".format(file2)) == True:
            print("{} file not present".format(file1))
            print("Skiping Deleteing {} file and deleting {} ...".format(file1, file2))
            os.system("rm {}".format(file2))
            return 2
        else:
            print("{} and {} are  not present".format(file1, file2))
            print("Skiping Deleteing files {} and {} ...".format(file1, file2))
            return 0

        return value
    elif value == 1:
        if os.path.isfile("{}".format(file1)) == True:
            print("Deleting specific files i.e {}   :/ .....".format(file1))
            os.system("rm {}".format(file1))
            return value
        else:
            print(
                "Deleting file {} failed because it does not exist ...:-(".format(file1))
            print("Skiping Deleteing {} file and continuing...  :-)".format(file1))
            return 0

    elif value == 2:
        if os.path.isfile("{}".format(file2)) == True:
            print("Deleting specific files i.e {}   :/ .....".format(file2))
            os.system("rm {}".format(file2))
            return value
        else:
            print(
                "Deleting file {} failed because it does not exist ...:-(".format(file2))
            print("Skiping Deleteing {} file and continuing...  :-)".format(file2))
            return 0
    elif value == 0:
        print("Skiping Deleteing files i.e {} :) .... and {} :) ....".format(
            file1, file2))
        return value
    else:
        print("THe specified files are not present in the current working directory")
        """warning"""
        return FileNotFoundError


def defaults_config(filename) -> dict:
    with open(filename, 'r') as config:
        config_json = json.load(config)
        logger.info("Using defaults_config configurations are : {}".format(
            config_json['inputs']))

        return config_json['inputs']


values = defaults_config("config.json")
logger_is = log_level(values['log_level'])
logger.info("Delete status returned {}".format(
    keep_delete_files("data.db", "log.txt", values['value'])))
conn = connection_to_database(values['database'])
# create_table()

check_database(logger_is, values['keep_delete'])
database_journal_model(conn, values['mode'])
typeof = type_of_signals(values['type_is'])
list_is = process_type(values['process_list_or_string'])

print("Starting pre checks ................")
checks()
print("starting the price checker...")

price1 = mp.Queue()

commits = mp.Queue()
logger.debug("queue created {} as price1".format(price1))
start1 = time.time()


num_processes = len(list_is)
curs = conn.cursor()


@logger.catch
def main(sender: mp.Queue or None):

    if typeof == "live":
        """if live mode use this process specifications the difference is we are isolating processes in different way(slightly) 
        sometimes"""
        if __name__ in ["__main__", "diff_checker"]:
            checker_processes = []
            changer_process = mp.Process(
                target=changer, args=(typeof, sender,))
            changer_process.start()
            tmp = 0
            for process in range(num_processes):
                if process+1 in list_is:
                    checker_processes.append(mp.Process(target=checker, args=(
                        start, all_differences[process], all_differences[process+1],)))
                    checker_processes[tmp].start()
                    tmp += 1
            changer_process.join()
            for process in range(len(list_is)):
                checker_processes[process].join()

    elif typeof == "historical":
        """if historical mode use this process specifications the difference is we are isolating processes in different way(slightly) 
        sometimes"""
        if __name__ == "diff_checker":
            checker_processes = []
            changer_process = mp.Process(
                target=changer, args=(typeof, sender,))
            commiter_process = mp.Process(target=commiter, args=())
            commiter_process.start()
            changer_process.start()
            tmp = 0
            for process in range(num_processes):
                if process+1 in list_is:
                    checker_processes.append(mp.Process(target=checker, args=(
                        start, all_differences[process], all_differences[process+1],)))
                    checker_processes[tmp].start()
                    tmp += 1

            for process in range(len(list_is)):
                checker_processes[process].join()
            changer_process.join()
            commiter_process.join()

# main(price1)
# print(process_type())
