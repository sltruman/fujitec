#!/usr/bin/env python3
import json
import os
import traceback
from pathlib import Path

from flask import Flask, request as req
from flask_cors import CORS
import xlrd
import threading

validing = None

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

        import test
  
        global validing     
        validing = threading.Thread(target=test.excel_to_json,args=[f'static/data/{filename}'])
        validing.start()
        
        return {'val':True, 'err':None}

@app.route('/fujitec/elevators-sync-status', methods=['GET'])
def elevators_sync_status():
    global validing
    print(validing)
    return {'val':'同步中...' if validing and validing.is_alive() else '同步结束','err':None}
    
        
print('http://localhost:60000/')
app.run(host='0.0.0.0', port=60000)
