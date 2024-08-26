import requests
import time, subprocess
import json, os, sys, inspect, csv
from rich import print_json
from colorama import init as colorama_init
from colorama import Fore
colorama_init(autoreset=True)
from datetime import datetime
from rich.table import Table
from rich.console import Console
from rich.box import SQUARE

from getDate import *
from retrain import *

rich_print = Console().print

def Exception_Handler(exec_info):
    sModuleInfo_Local = inspect.currentframe().f_code.co_name + " : " + inspect.getmodulename(__file__)
    exc_type, exc_obj, exc_tb = exec_info
    Error_Type = (
        (str(exc_type).replace("type ", ""))
        .replace("<", "")
        .replace(">", "")
        .replace(";", ":")
    )
    Error_Message = str(exc_obj)
    File_Name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    Function_Name = os.path.split(exc_tb.tb_frame.f_code.co_name)[1]
    Line_Number = str(exc_tb.tb_lineno)
    Error_Detail = (
        "Error Type ~ %s: Error Message ~ %s: File Name ~ %s: Function Name ~ %s: Line ~ %s"
        % (Error_Type, Error_Message, File_Name, Function_Name, Line_Number)
    )
    sModuleInfo = Function_Name + ":" + File_Name
    print(Fore.RED + "Following exception occurred: %s" % (Error_Detail))

from_ = None
to = None

from datetime import datetime
from datetime import datetime

def convert_date_to_datetime(date_str):
    """ Convert a string in 'yyyy-mm-dd' format to a datetime object. """
    return datetime.strptime(date_str, '%Y-%m-%d')

import os

def delete_csv_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted successfully.")
    except FileNotFoundError:
        print(f"File '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


import os
import pandas as pd

def append_or_create_csv(file1, file2):
    if os.path.exists(file1):
        df1 = pd.read_csv(file1)
        
        df2 = pd.read_csv(file2)
        
        combined_df = pd.concat([df1, df2], ignore_index=True)
        
        combined_df.to_csv(file1, index=False)
        print(f"Appended '{file2}' to '{file1}' successfully.")
    else:
        df2 = pd.read_csv(file2)
        df2.to_csv(file1, index=False)
        print(f"'{file1}' not found. Copied '{file2}' as '{file1}'.")




load_inquiry = pd.read_csv("inquiry.csv")
from  updateInq import *

def generate_time(stock):
    global from_, to
    
    if from_ is None:
        from_str = get_value_from_csv(stock, "db")
        if from_str:
            from_ = convert_date_to_datetime(from_str).timestamp()
        else:
            default_date = '2023-08-01'
            from_ = convert_date_to_datetime(default_date).timestamp()
        to = datetime.now().timestamp()
    else:
        fromn = datetime.fromtimestamp(from_)
        
        if fromn.month == 2:
            from_ = datetime.strptime(f"{fromn.year - 1}-08-01", '%Y-%m-%d').timestamp()
        else:
            from_ = datetime.strptime(f"{fromn.year}-02-01", '%Y-%m-%d').timestamp()
        
        to = from_


def amar_stock_api():
    list_of_stocks = [i["Scrip"] for i in requests.get("https://www.amarstock.com/LatestPrice/34267d8d73dd").json()]

    if not os.path.isdir(f"./DB_csv"):
        os.mkdir(f"./DB_csv")
    if not os.path.isdir(f"./DB_csv/temp_DB"):
        os.mkdir(f"./DB_csv/temp_DB")

    cntback = 10000000
    all_data = {}
    for stock in list_of_stocks[:]:
        try:
            cookie = '''.AspNet.ApplicationCookie=aX2aIdKyD9i0QA0Pa_8Z_1LnrS2obPJv_SFCHB25DRfwbFGx25lHXuDcbgMYa4DicI7m6NMiV4SV61EpjY8GVOhzBpWjm00RtxpVXcQ-d37KInvvTb1xYnmxvFNfBCmOuO-2Y-eYae2T7DJFLi8wtIdlg9I7D_OmyuxZj2JpnmOjYTiw_eDJme4oP4yQUIPtEMJ8tBdQpFF_qqoWIoajPMPD4NoO-DHP4KulyQ3rPVnvA1cFfFeAhcwG_apFdwGaTh5z7QcImA8PazxMI4hH-xGHZQ3YUrbm91hlUIK19jfNUEuQ6gi6HKMCBI6B1QZiNe2VY6FElvKLTDJVhzDRpQLagEkaCXBO_O0edcIOwtQKmgSAXeZxqw0pOLIpXPDuxcnPpq_xCDJXwmrKhSMtSsBGNfsw0vfytBdNfTl0kzWORUMfXqm3vSfJAVmm_4U4KunNQLVRXZofoCODQOfKIfa1iby4t4PQBoY6t3fzaHj6aScF-1Az8raCY_lz_1gODA1U2XC7T30gY4Nx1Ozl21mebGZaJBiMKofFWsWGt6uaRWKF'''
            data = {"t":[], "c":[], "o":[], "h":[], "l":[], "v":[]}
            global from_, to; from_, to = None, None
            while True:
                generate_time(stock)
                froms = datetime.fromtimestamp(from_).strftime('%Y-%m-%d %H:%M:%S')
                tos = datetime.fromtimestamp(to).strftime('%Y-%m-%d %H:%M:%S')
                print(Fore.CYAN + stock, " "*(20-len(stock)), froms, tos)

                url = f"https://www.amarstock.com/TradingView/History?resolution=1D&symbol={stock}&from={str(from_)}&to={str(to)}&countBack={str(cntback)}"
                
                amar_data = requests.get(url, headers={"Cookie": cookie}).json()
                if 'nextTime' in amar_data or amar_data['s'] != "ok":
                    print(f"No more Data for {stock}")
                    print_json(data=amar_data)
                    break
                for key in data: data[key] = amar_data[key] + data[key]
            all_data[stock] = data
            yourArray = all_data[stock]['t']
            if not (all(yourArray[item] <= yourArray[item + 1] for item in range(len(yourArray) - 1))):
                print(Fore.CYAN + stock, "is not sorted on time")
        except:
            Exception_Handler(sys.exc_info())
            print()
        try:
            with open(f"./DB_csv/temp_DB/{stock}.csv", 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["timestamp", "opening", "high", "low", "close", "adj_close", "volume"])
                writer.writeheader()
                data = all_data[stock]
                for i in range(len(data['t'])):
                    readable_time = datetime.fromtimestamp(data['t'][i]).strftime('%Y-%m-%d')
                    writer.writerow({
                        'timestamp': readable_time,
                        'opening': data['o'][i],
                        'high': data['h'][i],
                        'low': data['l'][i],
                        'close': data['c'][i],
                        'adj_close': data['c'][i],  # 'adj_close' is the same as 'close'
                        'volume': data['v'][i]
                    })
            print(f"File written:", Fore.MAGENTA + f"{stock}.csv")
        except:
            Exception_Handler(sys.exc_info())
            print()
        write_date =  str(from_).split(' ')[0]
        load_inquiry.loc[load_inquiry['share'] == stock, "model"] = write_date
        load_inquiry.loc[load_inquiry['share'] == stock, "db"] = write_date
        append_or_create_csv( f"./DB_csv/unadjusted_amarstock/{stock}.csv",f"./DB_csv/temp_DB/{stock}.csv")
        retrain_model(stock)

        delete_csv_file(f"./DB_csv/temp_DB/{stock}.csv")

        

    print()
    try:
        with open(f"./DB_csv/temp_DB/__summary__.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["no", "stock", "from", "to", "records"])
            writer.writeheader()
            for i, s in enumerate(all_data):
                if all_data[s]['t']:
                    writer.writerow({'no': i,
                                     'stock': s,
                                     'from': datetime.fromtimestamp(all_data[s]['t'][0]).strftime('%Y-%m-%d'),
                                     'to': datetime.fromtimestamp(all_data[s]['t'][-1]).strftime('%Y-%m-%d'),
                                     'records': len(all_data[s]['t'])
                                     })
    except:
        Exception_Handler(sys.exc_info())
        print()

load_inquiry.to_csv("inquiry.csv", index=False)

if __name__ == "__main__":
    amar_stock_api()
