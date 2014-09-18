# -*- coding: utf-8 -*-

from flask import Flask
from flask import g
from flask import abort

import logging
import settings

version = settings.__version__

app = Flask('app')
app.config.from_pyfile('settings.py', silent=True)

import rethinkdb as r
from rethinkdb import (RqlRuntimeError, RqlDriverError, RqlError)

import redis
red = redis.StrictRedis(host='localhost', port=6379, db=0)

logging.basicConfig(filename='Target.log', level=logging.DEBUG)
salt = settings.salt

app.config['ONLINE_LAST_MINUTES'] = settings.ONLINE_LAST_MINUTES
app.secret_key = settings.SECRET_KEY

from datetime import timedelta
app.permanent_session_lifetime = timedelta(minutes=5760)


from celery import Celery
from lib.AfricasTalkingGateway import (
    AfricasTalkingGateway, AfricasTalkingGatewayException)

celery = Celery('tasks', broker=settings.redis_broker)


@celery.task(ignore_result=True)
def welcomeMessage(to):
    logging.basicConfig(filename='SMS.log', level=logging.DEBUG)

    gateway = AfricasTalkingGateway(settings.username, settings.apikey)
    message = "Welcome to target limited, to purchase send TARGET *amount*business_id#  to 14014"

    try:
        recipients = gateway.sendMessage(to, message)
        for recipient in recipients:
            logging.info('number=%s;status=%s;messageId=%s;cost=%s'
                         % (recipient['number'], recipient['status'],
                            recipient['messageId'], recipient['cost']))

    except AfricasTalkingGatewayException, e:
        logging.warning('Database setup completed %s' % str(e))


@celery.task(ignore_result=True)
def send_notification_task(to, amount, balance, business_name):
    logging.basicConfig(filename='SMS.log', level=logging.DEBUG)

    gateway = AfricasTalkingGateway(settings.username, settings.apikey)
    message = " %s " % (amount, balance, business_name)

    try:
        recipients = gateway.sendMessage(to, message)
        for recipient in recipients:
            logging.info('number=%s;status=%s;messageId=%s;cost=%s'
                         % (recipient['number'], recipient['status'],
                            recipient['messageId'], recipient['cost']))

    except AfricasTalkingGatewayException, e:
        logging.warning('SMS failed to send %s' % str(e))


def dbSetup():
    connection = r.connect(host=settings.RDB_HOST, port=settings.RDB_PORT,
                           auth_key=settings.rethinkdb_auth)
    try:
        r.db_create(settings.TARGET_DB).run(connection)
        r.db(settings.TARGET_DB).table_create('User').run(connection)
        logging.info('Database setup completed')
    except RqlRuntimeError:
        logging.info('App database already exists')
    finally:
        connection.close()


@app.before_request
def before_request():
    try:
        logging.info('before_request')
        g.rdb_conn = r.connect(host=settings.RDB_HOST, port=settings.RDB_PORT,
                               db=settings.TARGET_DB, auth_key=settings.rethinkdb_auth)

    except RqlDriverError:
        logging.info('DB Connect Failed')
        abort(503, "No database connection could be established")


@app.teardown_request
def teardown_request(exception):
    try:
        logging.info('teardown_request')
        g.rdb_conn.close()
    except AttributeError:
        logging.info('Database failure - check your connection')


from clients import *
from distributors import *
