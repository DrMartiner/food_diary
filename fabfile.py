# -*- coding: utf-8 -*-

from fabric.api import *

env.use_ssh_config = True


@task
def pre():
    env.user = 'ubuntu'
    env.hosts = ['mypre']


@task
def collect_static():
    with cd('food_diary'):
        run('.virtualenv/bin/python manage.py collectstatic --noinput')


@task()
def deploy():
    with cd('food_diary'):
        run('git pull')
        run('sudo service uwsgi restart food_diary')
        run('.virtualenv/bin/pip install -r requirements.txt')
        run('.virtualenv/bin/python manage.py syncdb')
        run('.virtualenv/bin/python manage.py migrate')