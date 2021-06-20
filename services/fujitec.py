#!/usr/bin/env python3
import json
import os
import traceback
from pathlib import Path

from flask import Flask, request as req
from flask_cors import CORS
import threading

os.makedirs(f'db', exist_ok=True)

app = Flask(__name__, '')
CORS(app, send_wildcard=True)
app.config['JSON_AS_ASCII'] = False

@app.route('/fujitec/elevator', methods=['GET'])
def elevator():
    location = req.args['location']
    
    elevators = []

    for id in os.listdir(f'db/{location}') if os.path.exists(f'db/{location}') else []:
        try:
            with open(f'db/{location}/{id}',encoding='utf-8') as f:
                elevator = json.loads(f.read())
                elevators.append(elevator)
        except json.JSONDecodeError: continue
        except UnicodeDecodeError: continue
    return {'val': elevators, 'err': None}

@app.route('/fujitec/elevators-less', methods=['GET'])
def elevators_less():
    try:
        with open(f'db/primary.json', "r",encoding='utf-8') as f:
            primary = json.load(f)
    except:
        return {'val': [], 'err': None}

    val = []
    for location in os.listdir('db'):
        try:
            longitude,latitude,province,city = primary['locations'][location]
        except: continue

        elevators = os.listdir(f'db/{location}')
        maintaining_type = '即将我方保养'
        try:
            with open(f'db/{location}/{elevators[0]}',encoding='utf-8') as f:
                elevator = json.loads(f.read())
                maintaining_type = elevator['maintaining_type']
        except json.JSONDecodeError: continue
        except UnicodeDecodeError: continue

        val.append([longitude,latitude,len(elevators),maintaining_type,location,province,city])
    return {'val': val, 'err': None}

@app.route('/fujitec/elevators', methods=['GET'])
def elevators():
    try:
        with open(f'db/primary.json', "r",encoding='utf-8') as f:
            primary = json.load(f)
    except:
        return {'val': [], 'err': None}

    val = []
    for location in os.listdir('db'):
        try:
            longitude,latitude,province,city = primary['locations'][location]
        except: continue

        elevators = []
        for id in os.listdir(f'db/{location}'):
            try:
                with open(f'db/{location}/{id}',encoding='utf-8') as f:
                    elevator = json.loads(f.read())
                    elevators.append(elevator)
            except json.JSONDecodeError: continue
            except UnicodeDecodeError: continue

        val.append({
                'longitude':longitude,
                'latitude':latitude,
                'province':province,
                'city':city,
                'location':location,
                'elevators':elevators
            })
    return {'val': val, 'err': None}

@app.route('/fujitec/elevator-set', methods=['PUT'])
def elevator_set():
    args = req.get_json()
    location = args['location']
    id = args['id']
    type = args['type']
    maintaining_type = args['maintaining_type']
    service_life = args['service_life']

    elevator = {
        'id':id,
        'type':type,
        "maintaining_state":"已保养",
        "maintaining_type":maintaining_type,
        "service_life":service_life
    }

    try:
        with open(f'db/{location}/{id}.json', "w",encoding='utf-8') as f:
            primary = json.dump(elevator,f,ensure_ascii=False, indent=4)
    except:
        pass

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

        import db
        validing = threading.Thread(target=db.sync,args=[f'static/data/{filename}'])
        validing.start()
        
        return {'val':True, 'err':None}

@app.route('/fujitec/elevators-sync-status', methods=['GET'])
def elevators_sync_status():
    primary = {
        'locations':{},
        'status':'synced',
        'date':'2021-06-01',
        'count':0,
        'errors':[]
    }

    try:
        with open(f'db/primary.json', "r",encoding='utf-8') as f:
            primary = json.load(f)
    except:pass

    del primary['locations']
    return {'val':primary,'err':None}
        
@app.route('/fujitec/elevators-sync-date', methods=['GET'])
def elevators_sync_date():
    try:
        with open(f'db/primary.json', "r",encoding='utf-8') as f:
            primary = json.load(f)
    except:pass
    return {'val':primary['date'],'err':None}
        
print('http://localhost:60000/')
app.run(host='0.0.0.0', port=60000)
