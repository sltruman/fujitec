#!/usr/bin/env python3
import json
import os
import traceback
from pathlib import Path

from flask import Flask, request as req
from flask_cors import CORS
import xlrd

os.makedirs(f'db', exist_ok=True)

app = Flask(__name__, '')
CORS(app, send_wildcard=True)
app.config['JSON_AS_ASCII'] = False

@app.route('/fujitec/elevators', methods=['GET'])
def elevators():
    val = []
    for location in os.listdir('db'):
        elevators = []

        for id in os.listdir(f'db/{location}'):
            try:
                with open(f'db/{location}/{id}',encoding='utf-8') as f:
                    elevator = json.loads(f.read())
                    elevators.append(elevator)
            except json.JSONDecodeError:
                continue
            except UnicodeDecodeError:
                continue
        val.append({
            'location':location,
            'elevators':elevators
            })
    return {'val': val, 'err': None}

@app.route('/fujitec/elevator-set', methods=['PUT'])
def elevator_set():
    return { 'val':True, 'err':None}

from werkzeug.utils import secure_filename

app.config['UPLOAD_FOLDER'] = 'static/data/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/fujitec/elevators-valid', methods=['POST'])
def elevators_valid():
    if 'file' not in req.files:
        return {'val': None, 'err': '没有文件部分!'}

    file = req.files['file']
    if file.filename == '':
        return {'val': None, 'err': '没有选择文件!'}
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        import test
        test.excel_to_json('../doc/电梯信息0527.xls')

@app.route('/fujitec/elevators-sync', methods=['POST'])
def elevators_sync():
    if 'file' not in req.files:
        return {'val': None, 'err': '没有文件部分!'}

    file = req.files['file']
    if file.filename == '':
        return {'val': None, 'err': '没有选择文件!'}
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        #验证
        wb = xlrd.open_workbook_xls(filename)
        sheet = wb.sheet_by_index(0)
        rows = sheet.nrows
        err_list = []
        for i in range(2, rows):
            data = sheet.row_values(i)
            if not data[9]:
                if not data[0] and data[2]:
                    err_msg = f"第{i}行数据错误，缺少地址信息"
                    err_list.append(err_msg)
                continue
            continue
        if len(err_list) > 0:
            return {
                "val": False,
                "err": err_list
            }
        else:
            return {
                "val": True,
                "err": None
            }
        
        
print('http://localhost:60000/')
app.run(host='0.0.0.0', port=60000)
