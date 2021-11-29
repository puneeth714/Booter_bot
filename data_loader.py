import binance_data_handler as bdh
# import time
from datetime import date, timedelta
from diff_checker import logger, values
import json
import pairs
import os
import pandas as pd
from multiprocessing import Process, Queue
# all data files are checked from folder binance_data each file with specific convection
# base_url:str, coins:list or str, from_date:str, to_date:str, data_type:str, to_database:bool,add_all_data:bool


class data_load:
    def __init__(self, data_files_loc):
        # self.files = files
        # self.data = data
        self.data_files_loc = data_files_loc
        self.number_of_processes = []
        self.parameter = {}

    def parameters_handler(self, manual_config: str):
        if manual_config == "config":
            with open("historic.json", 'r') as each:
                params = json.load(each)
                for keys in params.keys():
                    if params[keys] == "":
                        if keys == "coins":

                            print(self.parameter_convention_handler())
                            if input("Want to enter coins or use pairs_list as default(Yes) ? otherwise No :  ") == "No":
                                if input("One or more coins : ").lower() == "one":
                                    params[keys] = [input(
                                        "Enter {} for data loading :".format(keys)).upper()]
                                else:
                                    print(
                                        "Enter the coins comma separated in upper case or lower case :  \n")
                                    pairs_list = input("")
                                    pairs_list = pairs_list.upper()
                                    pairs_list = pairs_list.split(sep=",")
                                    params[keys] = pairs_list
                            else:
                                print("using default (all coins ...")
                                params[keys] = pairs.pairs_list
                            continue
                        elif keys == "simulator_use_change":
                            continue
                        else:
                            print(keys+" is empty \n")

                            params[keys] = [input(
                                "Enter {} for data loading :".format(keys))]
                if "," in params["coins"] and type(params) != list:
                    params["coins"] = params["coins"].split(",")
                    params['coins'] = [(params['coins'])]
                    print(params)
            self.parameter = params
            return params
        elif manual_config == "manual":
            return self._extracted_from_parameters_handler_40()
    
    # TODO Rename this here and in `parameters_handler`
    def _extracted_from_parameters_handler_40(self):
        print("Enter manual parameters ...")
        print(self.parameter_convention_handler())
        parameters = {}
        with open("historic.json", 'r') as each:
            params = json.load(each)
            for keys in params.keys():
                parameters[keys] = input(
                    "Enter {} for data loading  :  ".format(keys))
            # print(parameters)
        self.parameter = parameters
        return parameters
    # base_url:str, coins:list or str, from_date:str, to_date:str, data_type:str, to_database:bool,add_all_data:bool

    def parameter_convention_handler(self):
        print("""
        base_url        =   https://data.binance.vision/data/spot/     (by default)
        coins           =   [coin_name,coin_name...] or list or input  (default)(list)
        from_date       =   yyyymmdd                                   (default)
        to_date         =   yyyymmdd                                   (default)
        data_type       =   aggTrades/trades/kline                     (default)(trades)
        to_database     =   True/False                                 (default)(False)
        add_all_data    =   True/False                                 (default)(False)
        files_per_process=  number of files to process by each process (default)(int:5)
        """)
    # parameters_handler()
    # parameter_convention_handler()

    def __estimate_number_of_files__(self):
        data_pars = self.parameter
        start_date = date(int(data_pars['from_date'][:4]), int(
            data_pars['from_date'][4:6]), int(data_pars['from_date'][6:8]))
        end_date = date(int(data_pars['to_date'][:4]), int(
            data_pars['to_date'][4:6]), int(data_pars['to_date'][6:8]))
        number_of_days = end_date-start_date
        number_of_coins = len(data_pars['coins'])
        return number_of_coins*(number_of_days.days+1)

    def __estimate_number_of_processes__(self):
        total_files = self.__estimate_number_of_files__()
        print("Number of process for {} files, each process utilizing {} files is : {} ".format(
            total_files, self.parameter['number_of_files_each_process'], 
            1 if int(total_files/int(self.parameter['number_of_files_each_process'])) == 0 
            else int(total_files/int(self.parameter['number_of_files_each_process']))+1))
        if total_files < int(self.parameter['number_of_files_each_process']):
            self.number_of_processes = 1
        else:
            self.number_of_processes = int(total_files/int(self.parameter['number_of_files_each_process']))+1

    def data_distribution(self, estimate=None):
        os.chdir((self.data_files_loc))
        if estimate is None:
            estimate = input(
                "Do you want to estimate_number_of_files(True/False) : ")
        if estimate == "True":
            total = self.__estimate_number_of_files__()
        else:
            total = len(os.listdir())

        self.__estimate_number_of_processes__()
        number_of_tasks_each_proccess = total / self.number_of_processes
        files_each_process = []
        if total >= self.number_of_processes:
            n = 0
            next1 = 0
            next1 = 0 if total % number_of_tasks_each_proccess == 0 else 1
            for _ in range(int(total/number_of_tasks_each_proccess+next1)):
                if total-n < number_of_tasks_each_proccess:
                    k = total-n
                    if n+1 == n+k:
                        files_each_process.append(int(n+1))
                    else:
                        files_each_process.append((int(n+1), int(n+k)))
                else:
                    files_each_process.append(
                        (int(n+1), int(n+number_of_tasks_each_proccess)))
                n += number_of_tasks_each_proccess
        else:
            files_each_process.append((0, total))
            os.chdir("../../")
            logger.info(files_each_process)
            return files_each_process
        os.chdir("../../")
        logger.info(files_each_process)
        return files_each_process

    def __get_all_files(self):
        os.chdir(self.data_files_loc)
        return [filename for filename in os.listdir()]

    def send_data(self, from_to: tuple, queue: Queue):
        # os.chdir(self.data_files_loc)
        files = self.__get_all_files()
        for filename in files:
            if filename in files[from_to[0]-1:from_to[1]]:
                # as files numbering is started from 1 in the
                # data_distributer we have to remove 1 here for correct file usage
                # print(files[from_to[0]:from_to[1]])
                # df = pd.read_csv(files, header=None)
                # files.append(df)
                queue.put(filename)
                # a=queue.get()
                # if a=="done":
                #     continue
                # else:
                #     print(a)
                #     exit("Error :/")
            else:
                continue
        queue.put_nowait("done")
        print("data_loader completed")
# check1=data_load("binance_data/extract_data", 5)
# print(check1.data_distribution())


def main_data_load() -> data_load:
    data_requester = data_load("binance_data/extract_data")
    data_requester.parameters_handler("config")
    files, status = bdh.main_data(
        data_requester.parameter, values['download_it'])
    print(status)
    return data_requester, files
