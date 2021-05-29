#!/usr/bin/env python3
import json
import os
import traceback
from pathlib import Path

from flask import Flask, request as req
from flask_cors import CORS
from agent import get_all_info, change_info, excel_to_json, data_verification

os.makedirs(f'db', exist_ok=True)

app = Flask(__name__, '')
CORS(app, send_wildcard=True)
app.config['JSON_AS_ASCII'] = False


@app.route('/fujitec/elevators', methods=['GET'])
def elevators():
    try:
        res = get_all_info()
        if res["val"]:
            elevators_data = res["data"]
        else:
            elevators_data = None
        return {'val': elevators_data, 'err': None}
    except Exception:
        err_msg = traceback.format_exc()
        print(err_msg)
        return {'val': None, 'err': err_msg}


@app.route('/fujitec/elevator-set', methods=['PUT'])
def elevator_set():
    try:
        data = json.loads(req.get_data())
        print(data)
        res_data = change_info(data)
        if res_data["val"] is True:
            return {'val': True, 'err': None}
        else:
            return {'val': False, 'err': res_data["err"]}
    except Exception:
        return {'val': False, 'err': traceback.format_exc()}


from werkzeug.utils import secure_filename

os.makedirs(f'static/data', exist_ok=True)

app.config['UPLOAD_FOLDER'] = 'static/data/'
@app.route('/fujitec/elevators-valid', methods=['POST'])
def elevators_valid():
    if 'file' not in req.files:
        return {'val': False, 'err': 'No file part!'}
    file = req.files['file']
    if file.filename == '':
        return {'val': False, 'err': 'No selected file!'}
    if file:
        filename = file.filename
        print(filename)
        file_path = app.config['UPLOAD_FOLDER'] + filename
        if os.path.exists(file_path):
            os.remove(file_path)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        res = excel_to_json(file_path)
        if res.get("val") is True:
            return {'val': True, 'err': None}
        else:
            return {"val": False, "err": res.get("err")}


@app.route('/fujitec/elevators-sync', methods=['POST'])
def elevators_sync():
    if 'file' not in req.files:
        return {'val': None, 'err': 'No file part!'}
    file = req.files['file']
    if file.filename == '':
        return {'val': None, 'err': 'No selected file!'}
    if file:
        filename = file.filename
        print(filename)
        file_path = app.config['UPLOAD_FOLDER'] + filename
        if os.path.exists(file_path):
            os.remove(file_path)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        res = data_verification(file_path)
        if res.get("val") is True:
            return {'val': True, 'err': None}
        else:
            return {"val": False, "err": res.get("err")}


print('http://localhost:60000/')
app.run(host='0.0.0.0', port=60000)
