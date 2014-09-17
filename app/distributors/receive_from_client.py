#! /usr/bin/env python
# -*- coding: utf-8 -*-

# res/ rep cycle

from app import app
from app import r
from app import g
from app import logging
from app import red
from app import RqlError
from flask import request


from app import welcomeMessage
from app import send_notification_task


#from: The number that sent the message
#to: The number to which the message was sent
#text: The message content
#date: The date and time when the message was received
#id: The internal ID that we use to store this message
#linkId - ?

@app.route('/oauthCallBack/', methods=['POST'])
def getTasks():

    if request.method != 'POST':
        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
            abort(400)

        text = request.json.get('text')

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

        resp = make_response(taskData, 200)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp
