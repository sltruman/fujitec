import os
import traceback

import xlrd
import json
from os import listdir


def get_all_info():
    """获取所有电梯信息
    res = {"err": None,
       "val":
           {"长沙华润置地广场一期": [{  # 电梯数2部                                                     C
               "location": "湖南长沙长沙华润置地广场一期",  # 电梯位置，由省份+城市+工程 名称拼接而成     M + N + C
               "id": "XAA9548",  # 电梯编号，独一无二                                               D
               "type": "其它类型梯",  # 电梯类型 F_SW扶梯，F_HS升降梯，其它类型梯                        F
               "maintaining_type": "第三方保养",  # 保养类型 我方保养，即将我方保养，第三方 保养：默认
               "maintaining_state": "未保养",  # 保养状态 已保养，未保养：默认
               "service_life": "10年"  # 使用年限 10年：默认
           }, {"location": "湖南长沙长沙华润置地广场一期",
               "id": "XAA9548", "type": "F_SW扶梯",
               "maintaining_type": "我方保养",
               "maintaining_state": "已保养",
               "service_life": "10年"}],
               "南长沙金轮时代广场": [{  # 电梯数1部
                   "location": "湖南长沙金轮时代广场",
                   "id": "XAA9550",
                   "type": "F_HS升降梯",
                   "maintaining_type": "第三方保养",
                   "maintaining_state": "未保养",
                   "service_life": "10年"}]}}
    """
    path = r"..\db"
    file_list = listdir(path)
    # print(file_list)
    elevators_info = {}
    for location in file_list:
        location_info = []
        file_path = r"{}\{}".format(path, location)
        # print(file_path)
        json_file = os.listdir(file_path)
        for json_name in json_file:
            j_path = r"{}\{}".format(file_path, json_name)
            j_info = open(j_path, encoding="utf-8")
            elevator_info = json.load(j_info)
            location_info.append(elevator_info)
            # print(elevator_info)
        elevators_info[location] = location_info
    print(elevators_info)
    return elevators_info
    # json_str = json.dumps(elevators_info, indent=4, ensure_ascii=False)
    # file_path1 = r"..\db\test.json"
    # with open(file_path1, "w+", encoding='utf-8') as json_file:
    #     json_file.write(json_str)


def change_info(data):
    try:
        location = data["location"]
        ele_id = data["id"]
        print(location, ele_id)
        if not location:
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


def excel_to_json(file_path):
    """excel文件内容转成json
    """
    wb = xlrd.open_workbook_xls(file_path)
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows
    for i in range(2, rows):
        data = sheet.row_values(i)
        name = data[2]
        name = name.replace(".", "")
        name = name.replace(" ", "")
        province = data[12]
        city = data[13]
        location = f"{province}{city}{name}"
        print(location)
        os.makedirs(r"..\db\{}".format(location), exist_ok=True)
        print(f"建立文件夹{location}成功")
        data_json = {
            "location": location,
            "id": data[3],
            "type": data[5],
            "maintaining_type": "我方保养",
            "maintaining_state": "已保养",
            "service_life": "10年"
        }
        json_str = json.dumps(data_json, indent=4, ensure_ascii=False)
        file_path2 = r"..\db\{}\{}.json".format(location, data[3])
        with open(file_path2, "w+", encoding='utf-8') as json_file:
            json_file.write(json_str)
            print(f"生成{data[3]}文件")
