import requests
import time
import os
import csv
import sys
import inspect
from datetime import datetime
from rich import print_json
from colorama import init as colorama_init
from colorama import Fore

colorama_init(autoreset=True)

def Exception_Handler(exec_info):
    exc_type, exc_obj, exc_tb = exec_info
    Error_Type = (str(exc_type).replace("type ", "")).replace("<", "").replace(">", "").replace(";", ":")
    Error_Message = str(exc_obj)
    File_Name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    Function_Name = os.path.split(exc_tb.tb_frame.f_code.co_name)[1]
    Line_Number = str(exc_tb.tb_lineno)
    Error_Detail = f"Error Type ~ {Error_Type}: Error Message ~ {Error_Message}: File Name ~ {File_Name}: Function Name ~ {Function_Name}: Line ~ {Line_Number}"
    print(Fore.RED + "Following exception occurred: %s" % (Error_Detail))

def generate_time(last_timestamp=None):
    if last_timestamp:
        from_ = int(time.mktime(datetime.strptime(last_timestamp, '%Y-%m-%d %H:%M:%S').timetuple()))
    else:
        from_ = int(time.mktime(datetime.strptime('2023-08-01 00:00:01', '%Y-%m-%d %H:%M:%S').timetuple()))
    to = int(time.mktime(datetime.strptime('2024-02-01 00:00:01', '%Y-%m-%d %H:%M:%S').timetuple()))
    return from_, to

def fetch_last_timestamp(file_path):
    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            last_row = None
            for last_row in reader:
                pass
            if last_row:
                return last_row['timestamp'] + " 00:00:01"
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

def amar_stock_api():
    list_of_stocks = [i["Scrip"] for i in requests.get("https://www.amarstock.com/LatestPrice/34267d8d73dd").json()]
    
    if not os.path.isdir(f"./DB_csv"):
        os.mkdir(f"./DB_csv")
    if not os.path.isdir(f"./DB_csv/unadjusted_amarstock"):
        os.mkdir(f"./DB_csv/unadjusted_amarstock")

    cntback = 10000000
    all_data = {}

    for stock in list_of_stocks[:]:
        file_path = f"./DB_csv/unadjusted_amarstock/{stock}.csv"
        last_timestamp = fetch_last_timestamp(file_path) if os.path.exists(file_path) else None
        
        from_, to = generate_time(last_timestamp)
        data = {"t": [], "c": [], "o": [], "h": [], "l": [], "v": []}
        
        try:
            while True:
                froms = datetime.fromtimestamp(from_).strftime('%Y-%m-%d %H:%M:%S')
                tos = datetime.fromtimestamp(to).strftime('%Y-%m-%d %H:%M:%S')
                print(Fore.CYAN + stock, " " * (20 - len(stock)), froms, tos)

                url = f"https://www.amarstock.com/TradingView/History?resolution=1D&symbol={stock}&from={str(from_)}&to={str(to)}&countBack={str(cntback)}"
                amar_data = requests.get(url).json()
                if 'nextTime' in amar_data or amar_data['s'] != "ok":
                    print(f"No more Data for {stock}")
                    print_json(data=amar_data)
                    break

                for key in data:
                    data[key] = amar_data[key] + data[key]
                    
                from_, to = generate_time(datetime.fromtimestamp(data['t'][0]).strftime('%Y-%m-%d %H:%M:%S'))

            all_data[stock] = data
            yourArray = all_data[stock]['t']
            if not (all(yourArray[item] <= yourArray[item + 1] for item in range(len(yourArray) - 1))):
                print(Fore.CYAN + stock, "is not sorted on time")
                
        except:
            Exception_Handler(sys.exc_info())
            print()

        try:
            mode = 'a' if os.path.exists(file_path) else 'w'
            with open(file_path, mode) as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["timestamp", "opening", "high", "low", "close", "adj_close", "volume"])
                if mode == 'w':
                    writer.writeheader()
                
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
            print(f"File written: {Fore.MAGENTA}{stock}.csv")
            
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
                    writer.writerow({
                        'no': i,
                        'stock': s,
                        'from': datetime.fromtimestamp(all_data[s]['t'][0]).strftime('%Y-%m-%d %H:%M:%S'),
                        'to': datetime.fromtimestamp(all_data[s]['t'][-1]).strftime('%Y-%m-%d %H:%M:%S'),
                        'records': len(all_data[s]['t']),
                    })
                else:
                    writer.writerow({
                        'no': i,
                        'stock': s,
                        'from': "",
                        'to': "",
                        'records': 0,
                    })
    except:
        Exception_Handler(sys.exc_info())
        print()

try:
    print("Start")
    amar_stock_api()
except:
    Exception_Handler(sys.exc_info())
    print()
print()
