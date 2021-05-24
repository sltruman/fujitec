#!/usr/bin/env python3
import copy
import json
import os
from flask import Flask, flash,abort, redirect, request as req, url_for
from flask_cors import CORS

os.makedirs(f'db', exist_ok=True)

app = Flask(__name__,'')
CORS(app,send_wildcard=True)
app.config['JSON_AS_ASCII'] = False

@app.route('/fujitec/elevators', methods=['GET'])
def elevators():
    return { 'val':[], 'err':None}

@app.route('/fujitec/elevator-set', methods=['PUT'])
def elevator_set():
    return { 'val': True,'err':None}

from werkzeug.utils import secure_filename
os.makedirs(f'static/data', exist_ok=True)

app.config['UPLOAD_FOLDER'] = 'static/data/'

@app.route('/fujitec/elevators-valid', methods=['POST'])
def elevators_valid():
    if 'file' not in req.files:
        err = 'No file part'
        return { 'val': None, 'err': 'No file part!' }
    file = req.files['file']
    if file.filename == '':
        return { 'val': None, 'err': 'No selected file!' }
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return { 'val': True, 'err': None }


@app.route('/fujitec/elevators_sync', methods=['POST'])
def elevators_sync():
    if 'file' not in req.files:
        err = 'No file part'
        return { 'val': None, 'err': 'No file part!' }
    file = req.files['file']
    if file.filename == '':
        return { 'val': None, 'err': 'No selected file!' }
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return { 'val': True, 'err': None }


print('http://localhost:60000/')
app.run(host='0.0.0.0',port=60000)
