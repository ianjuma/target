#!/usr/bin/env python

import os


def numCPUs():
    if not hasattr(os, 'sysconf'):
        raise RuntimeError('No sysconf detected.')
    return os.sysconf('SC_NPROCESSORS_ONLN')


bind = '127.0.0.1:8000'
workers = ( numCPUs() + 1 )
worker_class = 'gevent'
debug = False
daemon = True
pidfile = '/tmp/gunicorn.pid'
logfile = '/tmp/gunicorn.log'
accesslog = '/tmp/gunicorn-access.log'
preload = True
graceful_timeout = 30
proc_name = 'gunicorn-target'
spew = True
worker_connections = 1000
keepalive = 2
access_log_format = '"%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
limit_request_fields = 100
max_requests = 10000
