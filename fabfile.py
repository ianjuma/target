from fabric.api import (run, cd, local, env)

env.user = 'target'
env.hosts = ['178.62.249.236']


def setSupervisordLog():
    run('mkdir /var/log/supervisord/')


def startCelery():
    run('celery -A app.celery worker --loglevel=INFO --concurrency=10')


def supervisor():
    run('kill -9 `pgrep gunicorn`')
    run('kill -9 `pgrep supervisor`')
    run('kill -9 `pgrep celery`')
    run('export C_FORCE_ROOT="true"')
    run('supervisord -c /etc/supervisord.conf')


def setup_server(version):
    run('pty=False')
    run('mkdir /tmp/TaskWetu')
    with cd('/tmp/TaskWetu'):
        run('git clone https://github.com/nailab/taskwetu.git')
        with cd('/tmp/TaskWetu/taskwetu'):
            run('git checkout tags/%s' % (version,))
            result = run('pip install -r requirements.txt')
            if result.failed:
                local('GUNICORN failed')

            #prepare_deploy()


def prepare_deploy():
    run("apt-get update && apt-get -y dist-upgrade")
    run('apt-get clean && apt-get autoremove --purge --assume-yes')


def restartNginx():
    run('service nginx restart')


def deploy(version):
    setup_server(version)
    supervisor()
    restartNginx()
