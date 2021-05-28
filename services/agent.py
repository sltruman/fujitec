import datetime
import os
import time
import traceback

import requests
import xlrd
import json
import multiprocessing
from os import listdir
from services.config import gaode_api_key
from services.config import gaode_api_url


def get_all_info():
    """
    获取所有电梯信息
    """
    path = r"db"
    file_list = listdir(path)
    # print(file_list)
    elevators_info = []
    for location in file_list:
        file_path = r"{}\{}".format(path, location)
        json_file = os.listdir(file_path)
        j_name = json_file[0]
        j_path = r"{}\{}".format(file_path, j_name)
        info = open(j_path, encoding="utf-8")
        data = json.load(info)
        longitude = data["longitude"]
        latitude = data["latitude"]
        elevator = {
            "longitude": longitude,
            "latitude": latitude,
            "location": location,
        }
        location_info = []
        # print(file_path)
        json_file = os.listdir(file_path)
        for json_name in json_file:
            j_path = r"{}\{}".format(file_path, json_name)
            j_info = open(j_path, encoding="utf-8")
            elevator_info = json.load(j_info)
            location_info.append(elevator_info)
            # print(elevator_info)
        elevator["elevators"] = location_info
        elevators_info.append(elevator)
    print(elevators_info)
    return elevators_info


def change_info(data):
    try:
        location = data["location"]
        ele_id = data["id"]
        print(location, ele_id)
        if not location or ele_id:
            err_msg = "缺少必要参数"
            res_data = {
                "val": False,
                "err": err_msg
            }
            return res_data
        data_str = json.dumps(data, indent=4, ensure_ascii=False)
        file_path = r"../db/{}/{}".format(location, ele_id)
        with open(file_path, "w+", encoding="utf-8") as json_file:
            json_file.write(data_str)
            res_data = {
                "val": True,
                "err": None
            }
            return res_data
    except Exception as e:
        err_msg = traceback.format_exc()
        print(err_msg)
        res_data = {
            "val": False,
            "err": err_msg
        }
        return res_data


def data_verification(file_path):
    """数据验证"""
    wb = xlrd.open_workbook_xls(file_path)
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows
    err_list = []
    for i in range(2, rows):
        print(i)
        data = sheet.row_values(i)
        if not data[9]:
            if not data[0] and data[2]:
                err_msg = f"第{i}行数据错误，缺少地址信息"
                err_list.append(err_msg)
            continue
        continue
    if len(err_list) > 0:
        res_data = {
            "val": False,
            "err": err_list
        }
        return res_data
    else:
        res_data = {
            "val": True,
            "err": None
        }
        return res_data


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
    """excel文件内容转成json
    """
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
        location = f"{city}{name}"
        os.makedirs(r"../services/db/{}".format(location), exist_ok=True)
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
            file_path2 = r"../services/db/{}/{}.json".format(location, data[1])
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


# def write_json_file(file_path):
#     wb = xlrd.open_workbook_xls(file_path)
#     sheet = wb.sheet_by_index(0)
#     rows = sheet.nrows
#     times = rows // 500
#     for i in range(times + 1):
#         if i == times + 1:
#             start_row = times * 500
#             end_row = rows
#         else:
#             start_row = 2 + (i - 1) * 500
#             end_row = start_row + 500
#         p = multiprocessing.Process(target=excel_to_json, args=(file_path, start_row, end_row))
#         p.start()

# file_path = r"../services/static/data/电梯信息.xls"
# excel_to_json(file_path)
