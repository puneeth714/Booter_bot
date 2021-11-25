import pandas as pd
class pandas_data:
    def __init__(self,files_path,database_connection_or_db_file_path,dataframe_data):
        self.files_path = files_path
        self.database_connection_or_db_file= database_connection_or_db_file_path
        self.dataframe_data = dataframe_data
#present, check_with, to_check,signal1, upper, lower, symbol, work="diff", time_taken=None, time_type=time_type)

def pandas_data_is(df,data:list):
    df.loc[len(df.index)]=data

    dic_buy_sell_signal ={"time":[],"present":[], "to_check":[],"check_with":[],"symbol":[],"upper":[],"lower":[], "time_taken":[]}
    data_buy_sell_signal =pd.DataFrame(dic_buy_sell_signal)
