import sqlite3
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import plotly.express as px
import pandas as pd
import json
from loguru import logger
# import plotly.graph_objects as go
# pd.options.plotting.backend = 'plotly'


def connection_to_data(file) -> object:
    """connection to sqlite database in given location

    Args:
        file (str): file location (Absolute or relative path) This file should be present in database folder only

    Returns:
        object: connection object
    """

    return sqlite3.connect(file)


def extract_data(use, file, command) -> tuple:
    """extract query from file and if command is given return command

    Args:
        use ([type]): [description]
        file ([type]): [description]
        command ([type]): [description]

    Returns:
        tuple: [description]
    """
    if file is not None:
        return query_from_file(file)

    if command is not None:
        # use.execute(command)
        # return use.fetchall()
        return command
    coin = input('enter coin name: ')
    return """select time_fetch,present,signal,change from parameter where coin = '{}' """.format(
        coin
    )


def query_from_file(file: str) -> list or str:
    """if query should be taken from file this function is called

    Args:
        file (str): file path(Absolute or relative path)

    Returns:
        list or str: list of queries or a single query string
    """
    with open(file, 'r') as f:
        query = f.read()
        query.replace("\n", " ")
        if int(query.count(";")) > 1:
            queries = []
            for _ in range(int(query.count(";"))):
                queries.append(query[:query.index(';')])

                query = query[query.index(';')+1:]
            return queries
        return query
        # if type(queries) == list:
        #     values = []
        #     for query in queries:
        #         use.execute(query)
        #         values.append(use.fetchall())
        #     return values
        # use.execute(query)
        # return use.fetchall()


def parser(data: list) -> dict:
    """parses the data from query returned data to time values and signal list

    Args:
        data (list): data from query

    Returns:
        dict: a dictionary containing time values and signal values
    """

    data_parsed = {}

    if type(data[0]) == list:
        for i in range(len(data)):
            time = []
            value = []
            signal = []
            # time1=[]
            for j in range(len(data[i])):
                time.append(str(data[i][j][0]))
                value.append(data[i][j][1])
                signal.append(data[i][j][2])
            data_parsed[i] = [time, value, signal]
    else:
        time = []
        value = []
        signal = []
        for datum in data:
            time.append(str(datum[0]))
            value.append(datum[1])
            signal.append(datum[2])
            # time1.append([datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in time])
        data_parsed[0] = [time, value, signal]

    return data_parsed


def plot_data(values):
    time = []
    value = []
    signal = []
    for i in range(len(values)):
        # time, value, signal = values[i]
        if len(values[i][0]) == 0:
            continue
        # plt.plot(time, value)
        # plt.xlabel('Time')
        # plt.ylabel('Value')
        # plt.title('Signal')
        time.append(values[i][0])
        value.append(values[i][1])
        signal.append(values[i][2])
    plt.plot(time[0], value[0])
    plt.plot(time[1], value[1])
    plt.show()

    # for i in range(len(values)):
    #     time, value, signal=values[i]
    #     if len(values[i][0]) ==0:
    #         continue
    #     a=pe.scatter(values)
    # a.show()
    pass


def pandas_format(conn: sqlite3.Connection, queries: str or list) -> DataFrame:
    if type(queries) == list:
        df = []
        for i in range(len(queries)):
            try:
                df.append(pd.read_sql_query(queries[i], conn))
            except:
                continue
        return df

    elif type(queries) == str:
        df = pd.read_sql_query(queries, conn)
        return df


def pandas_plot(df: DataFrame or list):
    if type(df) == list:
        for i in range(len(df)):
            print(df[i].head())
            df[i]['time_fetch'] = pd.to_datetime(
                df[i]['time_fetch'], unit='ms')
            # df[i].plot(x='time_fetch', y='present')
            print(df[i]['time_fetch'])
            plt.plot(df[i]['time_fetch'], df[i]['present'])
            px.scatter(x=df[i]['time_fetch'], y=df[i]['present'])
        plt.show()

    elif type(df) == DataFrame:
        df.plot()
        df.show()


def plot_type() -> str or None:
    type = input(
        "Do you want to : \n 1)use commands from file\n 2)Enter commands\n 3)Use default command")
    if int(type) == 1:
        return input("FILE absolute or relative path : ")
    elif int(type) == 2:
        return input("Enter the query string : ")
    elif int(type) == 3:
        return None


def csv_data(filename: str):
    df = pd.read_csv(filename, header=None)
    print(df.head(10))
    # df[4] = pd.to_datetime(
    #             df[4], unit='ms')
    # print(df.head(10))
    # df=DataFrame(df)
    # # df=df.reindex(['count','price','change','volume','timestamp','maker','buyer'],axis=1)
    # print(df.head(10))
    # df=DataFrame("timestamp":df[4],"price":df[1])
    # df.plot(x=df['timestamp'],y=df['price'])
    # # df.show()
    # # df.plot()
    # plt.show()


def database_location(path_of_file=None) -> str:
    try:
        with open('config.json', 'r') as value:
            values = json.load(value)
            path_of_file = values['inputs']['plotter_database']

    except:
        logger.error("Could not load config.json")
    if path_of_file is None:
        path_of_file = input("database location(Absolute or relative path) : ")
    return path_of_file


def main():
    # csv_data("database/ETHUSD.csv")
    path_of_file = database_location()
    conn = connection_to_data("database/"+path_of_file)
    queries = extract_data(conn, 'plotter.sql', None)
    df = pandas_format(conn, queries)
    pandas_plot(df)


main()
