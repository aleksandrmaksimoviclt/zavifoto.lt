
from fabric.api import *
from fabric.context_managers import cd

env.hosts = ['root@46.101.161.158']
env.activate = 'source ../env/bin/activate'


def deploy():
    with cd('/web/zavi/zavifoto.lt/'):
        run('git pull origin master')
        with prefix(env.activate):
            run('pip install -r requirements.txt')
            run('python3 manage.py migrate')
            run('echo "yes\n" | python3 manage.py collectstatic')
    run('supervisorctl restart zavi')
    run('systemctl restart nginx')


def logs(file='*'):
    with cd('/web/zavi/logs/'):
        run('tail -f {}'.format(file))
