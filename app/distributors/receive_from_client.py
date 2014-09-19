#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (request, abort, jsonify, make_response)
from app import app
from app import r
from app import g
from app import logging
from app import red
from app import RqlError

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
    if request.method is 'POST':
        if request.headers['Content-Type'] != 'text/plain':
            abort(400)

        text = request.data
        sender = request.args.get('from')

        try:
            tasks = r.table('Client').get(sender).update(text).run(g.rdb_conn)
        except RqlError:
            logging.warning('DB code verify failed on /api/getTasks/')

            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        resp = make_response(tasks, 200)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp


def receivePayment():
    pass


@app.route('/api/getUSSD/', methods=['POST'])
def ussdCallBack():
    if request.method is 'POST':
        if request.headers['Content-Type'] != 'text/plain':
            abort(400)

        text = request.data

        # Reads the variables sent via POST from our gateway
        sessionId   = request.args.get("sessionId")
        serviceCode = request.args.get("serviceCode")
        phoneNumber = request.args.get("phoneNumber")
        text        = request.args.get("text")

        if request.args.get('text') is '':
            # load menu
            menu_text = """CON What would you like to do? \n
            1. To pay a distributor \n
            2. To check balance \n
            3. To make a credit request \n
            4. Check my transaction history \n
            """

            resp = make_response(menu_text, 200)
            resp.headers['Content-Type'] = "text/plain"
            resp.cache_control.no_cache = True
            return resp

        elif request.args.get('text') is '1':
            # pay a distributor
            balance = "END your balance is 2000 Kshs"

            resp = make_response(balance, 200)
            resp.headers['Content-Type'] = "text/plain"
            resp.cache_control.no_cache = True
            return resp

        elif request.args.get('text') is '2':
            balance = "END your balance is 2000 Kshs"
            resp = make_response(balance, 200)

            resp.headers['Content-Type'] = "text/plain"
            resp.cache_control.no_cache = True
            return resp

        elif request.args.get('text') is '2':
            balance = "END your balance is 2000 Kshs"
            resp = make_response(balance, 200)

            resp.headers['Content-Type'] = "text/plain"
            resp.cache_control.no_cache = True
            return resp
        else:
            balance = "END your balance is 2000 Kshs"
            resp = make_response(balance, 200)
            resp.headers['Content-Type'] = "text/plain"
            resp.cache_control.no_cache = True
            return resp

        try:
            tasks = r.table('Client').get(sender).update(text).run(g.rdb_conn)
        except RqlError:
            logging.warning('DB code verify failed on /api/getTasks/')

            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        resp = make_response(tasks, 200)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp



def displayMenu():
    menu_text = """CON What would you like to do? \n
            1. To pay a distributor \n
            2. To check balance \n
            3. To make a credit request \n
            4. Check my transaction history \n
            """
    return menu_text


def ussd_proceed(ussd_text):
    return "CON %s" %(ussd_text)


def ussd_stop(ussd_text):
    return "END %s" %(ussd_text)
