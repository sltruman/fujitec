
import datetime
import requests as http
import pandas as pd
import os
import json
import traceback

def sync(file_path):
    primary = {
        'locations':{},
        'status':'syncing',
        'date':'2021-06-01',
        'count':0,
        'errors':[]
    }

    try:
        with open(f'db/primary.json', "r",encoding='utf-8') as f:
            primary = json.load(f)
    except:
        traceback.print_exc()

    for i,row  in pd.read_excel(file_path,parse_dates=True).iterrows():
        locations = primary['locations']
        location = row['工程名']
        os.makedirs(f'db/{location}',exist_ok=True)

        if location in primary['errors']:
            continue

        try:    
            if location not in locations:
                print(location)
                res = http.get(url='https://restapi.amap.com/v3/geocode/geo?parameters', params={
                    "address": location,
                    "key": 'acfdf3007ee8263d577e40ee29427e75'
                })

                longitude,latitude = res.json()["geocodes"][0]['location'].split(",")
                locations[location] = longitude,latitude,row['省份'],row['地区']
        except:
            primary['errors'].append(location)
            continue
        else:
            longitude,latitude,_,_ = locations[location]

        #保养类型
        maintaining_type = row['维保状态']
        if maintaining_type == "代理商有偿保养" or  maintaining_type == "代理商免保中":
            maintaining_type = "代理商保养"
        elif maintaining_type == "其他公司保养":
            maintaining_type = "第三方保养"
        elif maintaining_type == "有偿保养中" or maintaining_type == "免保中":
            maintaining_type = "我方保养"
        else:
            maintaining_type = "即将我方保养"

        #扶梯类型判断
        elevator_type = row['机种类别']
        if elevator_type == "F/SW":
            elevator_type = "扶梯"
        elif elevator_type == "F/HS":
            elevator_type = "升降梯"
        else:
            elevator_type = "其它类型梯"

        try:
            service_life = row['免保开始日']
            service_life = str(datetime.datetime.now().year - datetime.datetime.strptime(str(service_life),'%Y-%m-%d %H:%M:%S').year)
        except:
            service_life = '不明'
        
        id = row['工程号']

        elevator = {
            'id':id,
            'type':elevator_type,
            "maintaining_state":"已保养",
            "maintaining_type":maintaining_type,
            "service_life":service_life
        }

        with open(f'db/{location}/{id}.json', "w",encoding='utf-8') as f:
            json.dump(elevator, f, ensure_ascii=False, indent=4)
        primary['count'] += 1

    primary['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    primary['status'] = 'synced'
    with open(f'db/primary.json', "w",encoding='utf-8') as f:
        json.dump(primary, f, ensure_ascii=False, indent=4)

sync(r'C:\Users\SLTru\Desktop\fujitec\doc\电梯信息0601.xls')