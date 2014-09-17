#! /usr/bin/env python
# -*- coding: utf-8 -*-

# res/ rep cycle

from app import app
from app import r
from app import g
from app import logging
from app import red
from app import RqlError
from app import session

from flask import make_response
from flask import jsonify
from flask import abort, request

from json import dumps

from app import new_task_message
from app import send_notification_task


@app.route('/api/getTasks/', methods=['POST', 'GET'])
def getTasks():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
        abort(400)

    username = request.json.get('username')

    if username not in session:
        return redirect('/')

    taskData = []
    try:
        tasks = r.table('Tasks').filter({"username": username}).run(g.rdb_conn)
        for data in tasks:
            taskData.append(data)

    except RqlError:
        logging.warning('DB code verify failed on /api/getTasks/')

        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    taskData = dumps(taskData)

    resp = make_response(taskData, 200)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp
