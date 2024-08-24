import requests
from bs4 import BeautifulSoup
import time, subprocess
import json, time, os,sys, inspect, ast, csv
from rich import print_json
from colorama import init as colorama_init
from colorama import Fore
colorama_init(autoreset=True)

from datetime import datetime

print_ = True
Date = '2023-02-12'
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

from rich.table import Table
from rich.console import Console
from rich.box import SQUARE
rich_print = Console().print

from_ = None
to = None

def generate_time():
    global from_, to
    if from_ is None:
        from_ = int(time.mktime(datetime.strptime('2023-08-01 00:00:01', '%Y-%m-%d %H:%M:%S').timetuple()))
        to = int(time.mktime(datetime.strptime('2024-02-01 00:00:01', '%Y-%m-%d %H:%M:%S').timetuple()))
    else:
        to = from_
        fromn = datetime.fromtimestamp(from_)
        froms = datetime.fromtimestamp(from_).strftime('%Y-%m-%d %H:%M:%S')
        if fromn.month == 2:
            from_ = int(time.mktime(datetime.strptime(f"{str(fromn.year - 1)}-08-01 00:00:01", '%Y-%m-%d %H:%M:%S').timetuple()))
        else:
            from_ = int(time.mktime(datetime.strptime(f"{str(fromn.year)}-02-01 00:00:01", '%Y-%m-%d %H:%M:%S').timetuple()))



def amar_stock_api():
    list_of_stocks = [i["Scrip"] for i in requests.get("https://www.amarstock.com/LatestPrice/34267d8d73dd").json()]
    # stock = "BERGERPBL"
    # list_of_stocks = ["GP", "BERGERPBL"]
    # readable_time = datetime.fromtimestamp(from_).strftime('%Y-%m-%d %H:%M:%S')
    # print(readable_time)

    if not os.path.isdir(f"./DB_csv"):
        os.mkdir(f"./DB_csv")
    if not os.path.isdir(f"./DB_csv/unadjusted_amarstock"):
        os.mkdir(f"./DB_csv/unadjusted_amarstock")

    cntback = 10000000
    all_data = {}
    for stock in list_of_stocks[:]:
        try:
            # cookie = '''ARRAffinity=1b1c50ba58ebe35ee2e5591f7bfc4da828e4e10037e76cd0a0bbde1be7653c74; g_state={"i_l":0}; __RequestVerificationToken=4RiltFMjGKtZP_mW8q8uxDNzv7oAZIAktTEE0IAS6LaIziywrnBjr2G7Y7TsMUCp4oBBMIB8O2CTNgZ8JCIVu6_RN4s1; .AspNet.ApplicationCookie=3gouTvh8w7yJ4Gb-cTEzlJq8RiduAGQMKv1DLVZy9fZseBr80SGUTbQxQQhL7oxL5pSuQy_vSqT5NmDI_5ja0BjWuzQ9uRD0x4SAuYUJgRdsbV3OUXB3RRA2LID-D_ZLxGhra1iT9F0NrIgMRsL9lC4EdnH-fmmM1bBGbApZO-RDtT31c61REE0E3Q55URxfvS2cjb-xng5f2STuOD-X-fMPj3Y-Fvf-ew6bCL0_0Hrl4tMN5si1mdOnwJr3QiATfxHUDGMuvTUlpt8TJ7YiizB836P5DAl_bhBO_lznjP_MGaqInN73gQxcuAGu_P09_5yRytdXruPYbYwBnTHcc739r0Wkq0_94nJGaScizpt1dp054imVXxViaJuS56q1wATIS0YRWemu0Oxa9yRMaXMH-k5EHgqira_YgFKh7jNMdPEjbZpHWRhy16g8ViTlPagqllD9YBlyakYkHSVZze7A8654kfF504PPP4AtMS3307qUSOQXOPviuBPMqGFu6dwewTQmoSj7rL6V3HUPI-Qkmlo'''
            cookie = '''.AspNet.ApplicationCookie=aX2aIdKyD9i0QA0Pa_8Z_1LnrS2obPJv_SFCHB25DRfwbFGx25lHXuDcbgMYa4DicI7m6NMiV4SV61EpjY8GVOhzBpWjm00RtxpVXcQ-d37KInvvTb1xYnmxvFNfBCmOuO-2Y-eYae2T7DJFLi8wtIdlg9I7D_OmyuxZj2JpnmOjYTiw_eDJme4oP4yQUIPtEMJ8tBdQpFF_qqoWIoajPMPD4NoO-DHP4KulyQ3rPVnvA1cFfFeAhcwG_apFdwGaTh5z7QcImA8PazxMI4hH-xGHZQ3YUrbm91hlUIK19jfNUEuQ6gi6HKMCBI6B1QZiNe2VY6FElvKLTDJVhzDRpQLagEkaCXBO_O0edcIOwtQKmgSAXeZxqw0pOLIpXPDuxcnPpq_xCDJXwmrKhSMtSsBGNfsw0vfytBdNfTl0kzWORUMfXqm3vSfJAVmm_4U4KunNQLVRXZofoCODQOfKIfa1iby4t4PQBoY6t3fzaHj6aScF-1Az8raCY_lz_1gODA1U2XC7T30gY4Nx1Ozl21mebGZaJBiMKofFWsWGt6uaRWKF'''
            data = {"t":[], "c":[], "o":[], "h":[], "l":[], "v":[]}
            global from_, to; from_,to = None, None
            while True:
                generate_time()
                froms = datetime.fromtimestamp(from_).strftime('%Y-%m-%d %H:%M:%S')
                tos = datetime.fromtimestamp(to).strftime('%Y-%m-%d %H:%M:%S')
                print(Fore.CYAN + stock, " "*(20-len(stock)), froms, tos)
                # for per minute data
                # url = f"https://www.amarstock.com/TradingView/History?resolution=1&symbol={stock}&from={str(from_)}&to={str(to)}&countBack={str(cntback)}"
                # for per day data 
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
            with open(f"./DB_csv/unadjusted_amarstock/{stock}.csv", 'w') as csvfile:
                # Adjust the order of fieldnames to match the desired sequence
                writer = csv.DictWriter(csvfile, fieldnames=["timestamp", "opening", "high", "low", "closing", "adj_close", "volume"])
                writer.writeheader()
                data = all_data[stock]
                for i in range(len(data['t'])):
                    readable_time = datetime.fromtimestamp(data['t'][i]).strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow({
                        'timestamp': readable_time,
                        'opening': data['o'][i],
                        'high': data['h'][i],
                        'low': data['l'][i],
                        'closing': data['c'][i],
                        'adj_close': data['c'][i],  # 'adj_close' is the same as 'closing'
                        'volume': data['v'][i]
                    })
            print(f"File written:", Fore.MAGENTA + f"{stock}.csv")
        except:
            Exception_Handler(sys.exc_info())
            print()

    print()
    try:
        with open(f"./DB_csv/unadjusted_amarstock/__summary__.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["no", "stock", "from", "to", "records"])
            writer.writeheader()
            for i, s in enumerate(all_data):
                if all_data[s]['t']:
                    writer.writerow({'no': i,
                                     'stock': s,
                                     'from': datetime.fromtimestamp(all_data[s]['t'][0]).strftime('%Y-%m-%d %H:%M:%S'),
                                     'to': datetime.fromtimestamp(all_data[s]['t'][-1]).strftime('%Y-%m-%d %H:%M:%S'),
                                     'records': len(all_data[s]['t']),
                                     })
                else:
                    writer.writerow({'no': i,
                                     'stock': s,
                                     'from': "",
                                     'to': "",
                                     'records': 0,
                                     })
    except:
        Exception_Handler(sys.exc_info())
        print()

def stock_now_api():
    list_of_stocks = [i["Scrip"] for i in requests.get("https://www.amarstock.com/LatestPrice/34267d8d73dd").json()]
    stock = "RECKITTBEN"
    list_of_stocks = ["RECKITTBEN"]
    from_ = int(time.mktime(datetime.strptime('2019-01-01 10:00:00', '%Y-%m-%d %H:%M:%S').timetuple()))
    to = int(time.mktime(datetime.strptime('2023-12-31 14:30:00', '%Y-%m-%d %H:%M:%S').timetuple()))
    # readable_time = datetime.fromtimestamp(from_).strftime('%Y-%m-%d %H:%M:%S')
    # print(readable_time)
    cntback = 10000000
    all_data = {}
    for stock in list_of_stocks:
        try:
            skip = 0; tmp_data = []; Break = False;
            while True:
                url = f"https://stocknow.com.bd/api/v1/instruments/{stock}/history?data2=true&resolution=1&skip={str(skip)}"
                stock_now_data = requests.get(url).json()
                for i in range(len(stock_now_data[0])):
                    if from_ <= stock_now_data[5][-i-1] <= to:
                        tmp_data = [[stock_now_data[k][-i-1] for k in range(6)]] + tmp_data
                    if from_ > stock_now_data[5][-i-1]:
                        Break = True
                if Break: break
                if not stock_now_data[0]:
                    print(datetime.fromtimestamp(tmp_data[-1][5]).strftime('%Y-%m-%d %H:%M:%S'))
                    Break = True
                skip += 300
                print(skip, len(tmp_data))
            all_data[stock] = tmp_data
        except:
            Exception_Handler(sys.exc_info())
            print()
    print()

    if not os.path.isdir(f"./DB_csv"):
        os.mkdir(f"./DB_csv")
    if not os.path.isdir(f"./DB_csv/unadjusted_stocknow_from_2019_to_2023"):
        os.mkdir(f"./DB_csv/unadjusted_stocknow_from_2019_to_2023")
    import csv

    for s in all_data:
        with open(f"./DB_csv/unadjusted_stocknow_from_2019_to_2023/{s}.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["timestamp", "closing", "opening", "high", "low", "volume"])
            writer.writeheader()
            data = all_data[s]
            for i in range(len(data['t'])):
                readable_time = datetime.fromtimestamp(data['t'][i]).strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow({'timestamp': readable_time, 'closing': data['c'][i], 'opening': data['o'][i], 'high': data['h'][i], 'low': data['l'][i], 'volume': data['v'][i]})




try:
    print("start")
    amar_stock_api()
    # stock_now_api()
except:
    Exception_Handler(sys.exc_info())
    print()
print()

