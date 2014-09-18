#!/usr/bin/env python

import os


def numCPUs():
    if not hasattr(os, 'sysconf'):
        raise RuntimeError('No sysconf detected.')
    return os.sysconf('SC_NPROCESSORS_ONLN')


use = 'app:app'
bind = '127.0.0.1:8000'
workers = (numCPUs() * 2 + 1)
worker_class = 'gevent'
backlog = 2048
debug = False
daemon = True
pidfile = '/tmp/gunicorn-target.pid'
logfile = '/tmp/gunicorn-target.log'
accesslog = '/tmp/gunicorn-target-access.log'
preload = True
graceful_timeout = 30
timeout = 60
proc_name = 'gunicorn-target'
proxy_protocol = False
spew = True
worker_connections = 1000
keepalive = 2
access_log_format = '"%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
limit_request_fields = 100
max_requests = 10000
