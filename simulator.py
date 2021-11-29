from numpy import empty
import time
import json
import sqlite3
from datetime import datetime
from binance_data_handler import binance_data
from tabulate import tabulate
from matplotlib import pyplot as plt
from ploter import simulator_plot


class simulator(binance_data):
    """simulator class
    """

    def __init__(self, default, asset_name, logging, database, change, table, freq, table_list_results):
        """constructor for simulator

        Args:
            default (float): how much of the asset
            asset_name (list): name(s) of the assets
            asset_price (float): price at which buying or selling
            how_much (float): how much money is investing
            only_one (bool): True if only one coin
            logging (integer): logging level for debugging
        """
        self.default = default
        self.asset_name = asset_name
        self.logging = logging
        self.database = database
        self.change = change
        self.table = table
        self.connection = None
        self.table_list_results = table_list_results
        self.cursor = None
        self.min_max = []
        self.all_market_pairs_balance = {}
        self.freq = freq
        self._plot_simulation_data_ = {}
        self.balance = self.__create_balance()
        self.__connection__()

    def __create_balance(self) -> dict:
        if len(self.asset_name) == 1:
            return {self.asset_name[0]: self.default}
        else:
            return {self.asset_name[i]: self.default for i in range(len(self.asset_name))}
        # for i in range(len(self.asset_name)):

    def __connection__(self):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def data(self):
        execute = self.query_generator()
        data = {}
        if len(execute) == 1:
            for each_days in execute[self.asset_name[0]].keys():
                self.cursor.execute(execute[self.asset_name[0]][each_days])
                tmp = {each_days: self.cursor.fetchall()}
                data[self.asset_name[0]] = tmp
        else:
            tmp = {}
            for i in execute.keys():
                for each_days in execute[i]:
                    self.cursor.execute(execute[i][each_days])
                    tmp[each_days] = self.cursor.fetchall()
                    if tmp[each_days] == []:
                        continue
                data[i] = tmp
                tmp = {}
        self.cursor.close()
        self.connection.close()
        return data

    def min_max_in_table(self):
        query = "select min(time) ,max(time) from {};".format(self.table)
        self.cursor.execute(query)
        min_max = self.cursor.fetchall()[0]
        if min_max[0] is None and min_max[1] is None:
            print("No data in table")
            exit(0)
        self.min_max = min_max

    def query_generator(self):
        data_query = {}
        query = {}
        if self.freq != "":
            dates = self.calculate()
            if len(self.asset_name) != 0:
                for i in range(len(self.asset_name)):

                    for date in dates.keys():
                        if self.change == "":

                            query[date] = "SELECT * FROM {} WHERE {} = '{}' and {}>{} and {}<{}".format(
                                self.table, "market_pair", self.asset_name[i], "time", dates[date][0], "time", dates[date][len(
                                    dates[date])-1]
                            )
                        elif type(self.change) == list:
                            change_query = "".join(
                                "{} = {} or ".format("lower", str(each_change))
                                for each_change in self.change
                            )
                            change_query = change_query[:-3]

                            query[date] = "SELECT * FROM {} WHERE {} = '{}' and {} and {}>{} and {}<{}".format(
                                self.table, "market_pair", self.asset_name[i], change_query, "time", dates[date][0], "time", dates[date][len(
                                    dates[date])-1]
                            )
                        else:
                            query[date] = "SELECT * FROM {} WHERE {} = '{}' and {} ={} and {}>{} and {}<{}".format(
                                self.table, "market_pair", self.asset_name[i], "lower", self.change, "time", dates[date][0], "time", dates[date][len(
                                    dates[date])-1]
                            )

                    data_query[self.asset_name[i]] = query
                    query = {}
                print(data_query)
                return data_query
                # need to check this code
                # there is no need of below statements
        elif len(self.asset_name) != 1:
            for i in range(len(self.asset_name)):
                if self.change == "":

                    query = "SELECT * FROM {} WHERE {} = '{}'".format(
                        self.table, "market_pair", self.asset_name[i]
                    )
                else:
                    query = "SELECT * FROM {} WHERE {} = '{}' and {} ={}".format(
                        self.table, "market_pair", self.asset_name[i], "lower", self.change
                    )
                data_query[self.asset_name[i]] = query
            return data_query
        if len(self.asset_name) == 1 and self.change == "":
            data_query[self.asset_name[0]] = "SELECT * FROM {} WHERE {} = '{}' ".format(
                self.table, "market_pair", self.asset_name[0])
        else:
            data_query[self.asset_name[0]] = "SELECT * FROM {} WHERE {} = '{}' and {} = {}".format(
                self.table, "market_pair", self.asset_name[0], "lower", self.change)

    def simulate_signals(self):
        #Need to remove space constraint variables
        #each_parameter_balance_simulator can be used in place of each_parameter_balance and so on... (names containing 
        # simulator can be used insted in many aspects of this function)
        balance = self.balance
        data = self.data()
        each_parameter_balance = {}
        each_parameter_balance_simulator = {}
        all_market_pairs_balance = {}
        for each_balance in balance.keys():
            dates = {}
            data_simulate_dates = {}
            for data_in in data[each_balance].keys():
                for each_data in data[each_balance][data_in]:
                    if each_data[5] not in each_parameter_balance.keys():
                        each_parameter_balance[each_data[5]
                                               ] = balance[each_balance]
                        each_parameter_balance_simulator[each_data[5]] = [
                            [], []]
                        # self._plot_simulation_data_[each_balance]={data_in:{each_data[5]:[[each_data[0],balance[each_balance]]]}}

                    each_parameter_balance[each_data[5]] = self._updater_(
                        each_data[2], each_parameter_balance[each_data[5]])
                    each_parameter_balance_simulator[each_data[5]][0].append(
                        each_data[0])
                    each_parameter_balance_simulator[each_data[5]][1].append(
                        each_parameter_balance[each_data[5]])
                    # self._plot_simulation_data_[each_balance][data_in][each_data[5]].append([each_data[0],each_parameter_balance[each_data[5]]])

                    # plt.plot(each_data[0], each_parameter_balance[each_data[5]])
                    # self._plot_simulation_data_[0].append(each_data[0])
                    # self._plot_simulation_data_[1].append(each_parameter_balance[each_data[5]])
                # plt.show()
                dates[data_in] = each_parameter_balance
                data_simulate_dates[data_in] = each_parameter_balance_simulator
                del each_parameter_balance
                each_parameter_balance = {}
            all_market_pairs_balance[each_balance] = dates
            self._plot_simulation_data_[each_balance] = data_simulate_dates
        self.all_market_pairs_balance = all_market_pairs_balance

    def _updater_(self, change, balance):
        return balance+balance*change/100

    def _plotter_(self):
        simulator_plot(self._plot_simulation_data_)

    def simulate_results(self):  # sourcery no-metrics
        self.min_max_in_table()
        self.simulate_signals()
        print("Start time {} \nEnd time {}".format(
            self.min_max[0], self.min_max[1]))
        # sort the values in self.each_parameter_balance dictionary in descending order
        if "sort" in self.table_list_results:
            for each_market in self.all_market_pairs_balance:
                for each_date in self.all_market_pairs_balance[each_market]:
                    self.all_market_pairs_balance[each_market][each_date] = sorted(
                        self.all_market_pairs_balance[each_market][each_date].items(), key=lambda x: x[1], reverse=True)
                    # self.each_parameter_balance=sorted(self.each_parameter_balance.items(), key=lambda x: x[0])
                    self.all_market_pairs_balance[each_market][each_date] = dict(
                        self.all_market_pairs_balance[each_market][each_date])
        else:
            print("No sorting of results")
        if self.table_list_results == "list":
            for each_market in self.all_market_pairs_balance:
                for each_date in self.all_market_pairs_balance[each_market]:
                    print("Market pair : {}".format(each_market))
                    print("Date : {}".format(each_date))
                    for keys, value in self.all_market_pairs_balance[each_market][each_date].items():
                        print("     For change {} balance  became {}".format(
                            keys, value))
                    print("\n")
        elif "table" in self.table_list_results:
            table_format = self.table_list_results[self.table_list_results.index(
                "-")+1:]
            if table_format == "html":
                with open("results.html", "w") as f:
                    f.write(tabulate(self.tables(), headers=[
                        "Market Pair", "parameter", "Balance", "Balance after update", "Change"], tablefmt=table_format))
            else:
                print(tabulate(self.tables(), headers=[
                    "Market Pair", "parameter", "Balance", "Balance after update", "Change"], tablefmt=table_format))
        elif self.table_list_results == "csv":
            import csv
            with open('results.csv', 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Market Pair", "parameter",
                                "Balance", "Balance after update", "Change"])
                for each_market in self.all_market_pairs_balance:
                    for each_date in self.all_market_pairs_balance[each_market]:
                        for keys, value in self.all_market_pairs_balance[each_market][each_date].items():
                            writer.writerow(
                                [each_market, keys, value, value+value*keys/100, keys])
        elif self.table_list_results == "json":
            import json
            with open('results.json', 'w') as jsonfile:
                json.dump(self.all_market_pairs_balance, jsonfile, indent=4)

        else:
            print(
                "Please enter table or list in table_list_results parameter of historic.json ")
        if "(plot)" in self.table_list_results:
            self._plotter_()
        else:
            print("No plot")

    def tables(self):
        table = []
        for market in self.all_market_pairs_balance.keys():
            for each_date in self.all_market_pairs_balance[market].keys():
                for each_change in self.all_market_pairs_balance[market][each_date].keys():
                    table.append([market, each_change, self.balance[market], self.all_market_pairs_balance[market][each_date]
                                 [each_change], self.all_market_pairs_balance[market][each_date][each_change]-self.balance[market]])
        if "sort" in self.table_list_results:
            table.sort(key=lambda x: x[3], reverse=True)
        return table

    def calculate(self):
        days_frequency = (
            self.min_max[1]-self.min_max[0])/(int(self.freq)*24*60*60*1000)
        if int(days_frequency) == 0:
            return {1: [self.min_max[0], self.min_max[1]]}
        dates = {}
        present = self.min_max[0]
        for i in range(int(days_frequency)):
            dates[i+1] = [present, present+self.freq*60*60*24*1000]
            present = present+self.freq*60*60*24*1000
            if present > self.min_max[1]:
                dates[i+1][1] = self.min_max[1]
                break
        return dates


def config():
    # read the json file 'historic.json'
    with open('historic.json', 'r') as f:
        return json.load(f)


# [data["simulator_database"],data["simulator_use_change"],data["coins"],data["from_data"],data["to_data"]]
data_config = config()
simulator_is = simulator(default=1000, asset_name=data_config["coins"], logging=0,
                         database=data_config["simulator_database"], change=data_config["simulator_use_change"],
                         table=data_config["simulator_table_to_use"], freq=data_config["days_frequency"], table_list_results=data_config["table_list_results"])

simulator_is.simulate_results()
