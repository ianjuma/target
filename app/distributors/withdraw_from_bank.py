#! /usr/bin/env python
# -*- coding: utf-8 -*-

# res/ rep cycle

from app import app
from app import r
from app import g
from app import logging
from app import red
from app import RqlError


from app import welcomeMessage
from app import send_notification_task


def withdraw(username):
    try:
        user = r.table('Admin').get(username).run(g.rdb_conn)
    except Exception, e:
        logging.warning('DB failed on /admin/ -> user not found')
        raise e

    if user is None:
        pass