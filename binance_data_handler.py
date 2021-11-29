# from queue import Queue
from this import d
import requests
import shutil
from datetime import date, timedelta
# from data_loader import parameter_convention_handler
from pairs import pairs_list
import os
import re
import zipfile
from diff_checker import logger


class binance_data:
    def __init__(self, base_url: str, coins: list or str, from_date: str, to_date: str, data_type: str, to_database: bool, add_all_data: bool):
        self.base_url = base_url
        self.coins = coins
        self.from_date = from_date
        self.to_date = to_date
        self.data_type = data_type
        self.to_database = to_database
        self.add_all_data = add_all_data
        self.files = []
        self.downloads = []
        self.extract_data_files = []
        self.keep=[]

    def download_data(self):
        urls = self.url_generator()
        for each_url in urls:
            logger.info("using url {} ".format(each_url))
            if self.filename_convention(each_url)[0]+".zip" in self.extract_data_files:
                logger.info("skipping download of {}".format(each_url))
                continue
            # each_url="https://data.binance.vision/data/spot/daily/aggTrades/SCRTBUSD/SCRTBUSD-aggTrades-2021-10-23.zip"
            data = requests.get(each_url, stream=True)
            logger.info("requests response: {}".format(data))
            if data.status_code == 200:
                file_obj = self.file_write(each_url)
                logger.info("write file: {}".format(file_obj))
                shutil.copyfileobj(data.raw, file_obj)
                file_obj.close()
                logger.debug("Downloading status_code {}".format(data.status_code))
            self.extract_data_files.append(self.filename_convention(each_url)[0]+".zip")
            # exit(0)

    def decompress_data(
            self):
        # os.chdir("binance_data")
        for files in os.listdir():
            if os.path.isfile(files)  and files in self.extract_data_files and files not in self.keep:
                logger.info("extracting {}".format(files))
                # if files[] in self.extract:
                #     continue
                with zipfile.ZipFile(files) as file_instance:
                    file_instance.extractall("extract_data")
                self.keep.append(files[:-3]+"csv")    
    def remove_unwanted_extracted(self):
        os.chdir("extract_data")
        for file in os.listdir():
            if file not in self.keep:
                logger.info("removing file {}".format(file))
                try:
                    os.remove(file)
                except FileNotFoundError:
                    logger.info("the file {} does not exist\nContinuing...".format(file))
        logger.info("Files in current working directory {}".format(os.listdir()))
        os.chdir("../")
        # os.chdir("../")

    def url_generator(self):
        # https://data.binance.vision/data/spot/daily/aggTrades/ETHUSDT/ETHUSDT-aggTrades-2021-10-10.zip
        # base url is https://data.binance.vision/
        url = []
        if type(self.coins) == str:
            self.coins = self.coins.split(',')
        for coin in self.coins:
            for single_date in self.daterange():
                url_each = "{}/data/spot/daily/{}/{}/{}-{}-{}.zip".format(
                    self.base_url, self.data_type, coin, coin, self.data_type, single_date)
                url.append(url_each)
                # print(url_each)
        return url

    def previous_download(self):
        os.chdir("binance_data/extract_data")
        self.files = os.listdir()
        os.chdir("../../")

    def date_or_month(self):
        pass

    def cancatenate_data(self):
        pass

    def database_write(self):
        pass

    def filename_convention(self, url):
        return re.findall("([A-Z]*-[a-zA-Z]*[-0-9]*)", url)

    def exception_handler(self):
        pass

    def file_write(self, url):
        file_name = self.filename_convention(url)
        file_name = file_name[0]
        self.files.append(file_name)
        # os.chdir("binance_data")
        place_of = self.files.index(file_name)
        return open(self.files[place_of]+".zip", 'wb')

    def file_name_convention_print(self):
        # ETHUSDT-aggTrades-2021-10-10.zip
        # coins_name-trades_type-year-month-day.csv
        print("""Download data : {}-{}-{}-{}-{}.{}\nExtracted data   : {}-{}-{}-{}-{}.{}
            """.format("coins", "trades_type", "year", "month", "day", "file_extension(zip)", "coins", "trades_type", "year", "month", "day", "file_extension(csv)"))

    def get_file_names(self):
        print(self.file_name_convention_print())
        # extract_names = []
        # download_names = []
        names = []
        for symbols in self.coins:
            for dates in self.daterange():
                names.append(("{}-{}-{}.zip".format(symbols, self.data_type, dates),
                             ("{}-{}-{}.csv".format(symbols, self.data_type, dates))))
                # extract_names.append(
                #     "{}-{}-{}.csv".format(symbols, self.data_type, dates))
                # download_names.append(
                #     "{}-{}-{}.zip".format(symbols, self.data_type, dates))

        # return extract_names, download_names
        return names

    def files_check_extract(self):
        try:
            os.chdir("binance_data/extract_data")
        except:
            os.mkdir("binance_data/extract_data")
            os.chdir("binance_data/extract_data")
        # extract_names, download_names = self.get_file_names()
        names = self.get_file_names()
        keep = []
        download_files = []
        extract_data_files = []
        if len(os.listdir()) and len(os.listdir("../")) == 1:
            print("No files present in binance_data/extract_data")
            for filename in names:
                download_files.append(filename[0])
        else:

            for filename in names:
                if filename[1] in os.listdir():
                    keep.append(filename[1])
                    if filename[0] in os.listdir("../"):
                        extract_data_files.append(filename[0])

                elif filename[0] in os.listdir("../"):
                    extract_data_files.append(filename[0])
                else:
                    download_files.append(filename[0])
            self.keep = keep

        self.extract_data_files = extract_data_files
        self.downloads = download_files
        # self.extract = extract_data_files
        # return [keep, extract_data_files, download_files]
        return {'keep': keep, 'extract_data_files': extract_data_files, 'download_files': download_files}
            # for file_name in os.listdir():
            #     if file_name in extract_names:
            #         keep.append(file_name)
            # for file_name in os.listdir():
            #     if file_name in keep:
            #         continue
            #     else:
            #         os.remove(file_name)

    def logging_debug(self):
        pass

    def daterange(self):
        startyear = int(self.from_date[:4])
        startmonth = int(self.from_date[4:6])
        startday = int(self.from_date[6:8])
        to_year = int(self.to_date[:4])
        to_month = int(self.to_date[4:6])
        to_day = int(self.to_date[6:8])
        start_date = date(startyear, startmonth, startday)
        end_date = date(to_year, to_month, to_day+1)
        for n in range(int((end_date-start_date).days)):
            yield start_date + timedelta(n)


# check1 = binance_data("https://data.binance.vision", pairs_list,
#                       "20210901", "20210901", "aggTrades", False, False)
# for single_date in check1.daterange():
#     print(single_date)
# check1.url_generator()
# check1.file_write(
#     "https://data.binance.vision/data/spot/daily/aggTrades/SCRTBUSD/SCRTBUSD-aggTrades-2021-09-01.zip")
# check1.download_data()
# check1.decompress_data()
def main_data(configuration: dict, download_it=None):
    # sourcery skip: extract-method, hoist-statement-from-if, none-compare
    # if input("Do you want to Download the data again using config or use previous data(True/False) ? ") == "False":
    data_download_extract = binance_data(configuration['base_url'], configuration['coins'], configuration['from_date'],
                                         configuration['to_date'], configuration['data_type'], ['to_database'], configuration['add_all_data'])
    conf_list = data_download_extract.files_check_extract()
    os.chdir("../../")

    for keys in conf_list.keys():
        print(keys, " : ", conf_list[keys])

    if download_it == None:
        print("Do you want to continue with {} or want to download {} also as per the configuration ?\n".format(
            conf_list['keep'], conf_list['download_files']))
        print("Yes to download No to continue : \n")
        download_it = input("")

        # logger.info("")
    if download_it == "Yes":
        logger.info("Downloading status set to {}".format(download_it))
        logger.info("Trying to download files from {}".format(
            conf_list['download_files']))
        os.chdir("binance_data")

        data_download_extract.download_data()
        os.chdir("../")
        os.chdir("binance_data")
        data_download_extract.decompress_data()
        data_download_extract.remove_unwanted_extracted()
        os.chdir("../")
        return data_download_extract.files, True
    else:
        logger.info("No to downloads to happen")
        logger.info("Skip to download \n continue ")
        return data_download_extract.files, True
