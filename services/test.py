import datetime
import os
import time
import traceback

import requests
import xlrd
import json
import multiprocessing
from os import listdir

gaode_api_key = "acfdf3007ee8263d577e40ee29427e75"
gaode_api_url = "https://restapi.amap.com/v3/geocode/geo?parameters"

def type_judge(data):
    """扶梯类型判断"""
    if data == "F/SW":
        ele_type = "扶梯"
    elif data == "F/HS":
        ele_type = "升降梯"
    else:
        ele_type = "其它类型梯"
    return ele_type

def maintaining_type_judge(data):
    """保养类型"""
    if data == "代理商有偿保养" or "代理商免保中":
        maintaining_type = "代理商保养"
    elif data == "其他公司保养":
        maintaining_type = "第三方保养"
    elif data == "有偿保养中" or "免保中":
        maintaining_type = "我方保养"
    else:
        maintaining_type = "即将我方保养"
    return maintaining_type

def excel_to_json(file_path):
    time_start = time.time()
    wb = xlrd.open_workbook_xls(file_path)
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows
    err_msg = []
    for i in range(2, rows):
        print(i)
        data = sheet.row_values(i)
        print(data)
        name = data[2]
        name = name.replace(".", "")
        name = name.replace(" ", "")
        city = data[0]
        location = f"{name}"
        os.makedirs("../services/db/{}".format(location), exist_ok=True)
        params = {
            "address": location,
            "key": gaode_api_key
        }
        res = requests.get(url=gaode_api_url, params=params)
        req_data = res.json()
        r = req_data["geocodes"]
        if not r:
            print(f"{location}地址无效")
            err_msg.append(location)
        else:
            re = r[0]
            longitude_latitude = re["location"]
            longitude_latitude = longitude_latitude.split(",")
            longitude = longitude_latitude[0]
            latitude = longitude_latitude[1]
            local_year = datetime.datetime.now().year
            exemption_time = data[6]
            print(exemption_time)
            if exemption_time == "-" or not exemption_time:
                service_life = "不明"
            else:
                exemption_time = xlrd.xldate.xldate_as_datetime(sheet.cell(i, 6).value, 0).year
                service_life = local_year - exemption_time
            ele_type = type_judge(data[3])
            maintaining_type = maintaining_type_judge(data[4])
            data_json = {
                "city": city,
                "longitude": longitude,
                "latitude": latitude,
                "id": data[1],
                "type": ele_type,
                "maintaining_type": maintaining_type,
                "maintaining_state": "已保养",
                "service_life": service_life
            }
            json_str = json.dumps(data_json, indent=4, ensure_ascii=False)
            file_path2 = "../services/db/{}/{}.json".format(location, data[1])
            with open(file_path2, "w+", encoding='utf-8') as json_file:
                json_file.write(json_str)
    if err_msg:
        res_data = {
            "val": False,
            "err": err_msg
        }
    else:
        res_data = {
            "val": True,
            "err": None
        }
    time_end = time.time()
    print('totally cost', time_end - time_start)
    return res_data
