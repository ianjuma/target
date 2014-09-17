#! /usr/bin/env python
# -*- coding: utf-8 -*-

# res/ rep cycle

from app import app
from app import r
from app import g
from app import logging
from app import salt
from app import red
from app import RqlError


from app import welcomeMessage
from app import send_notification_task


@app.route('/admin/', methods=['POST', 'GET'])
def adminSign():
    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
            abort(400)

        username = request.json.get('username')
        password = request.json.get('password')

        try:
            user = r.table('Admin').get(username).run(g.rdb_conn)
        except Exception, e:
            logging.warning('DB failed on /admin/ -> user not found')
            raise e

        if user is None:
            resp = make_response(jsonify({"Not Found": "User Not Found"}), 404)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        session[username] = username

        resp = make_response(jsonify({"OK": "Signed In"}), 200)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    return render_template('adminSignin.html')
