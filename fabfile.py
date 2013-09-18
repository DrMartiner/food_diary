# -*- coding: utf-8 -*-

from fabric.api import *

env.use_ssh_config = True

BIN_PATH = '.env/bin/'
PROJECT_DIR = 'food_diary'

@task
def pre():
    env.user = 'ubuntu'
    env.hosts = ['mypre']


@task
def pull():
    with cd(PROJECT_DIR):
        run('git pull')


@task
def install():
    with cd(PROJECT_DIR):
        run('%spip install -r requirements.txt' % BIN_PATH)


@task
def restart():
    with cd(PROJECT_DIR):
        run('sudo service uwsgi restart food_diary')


@task
def collect():
    with cd(PROJECT_DIR):
        run('%spython manage.py collectstatic --noinput' % BIN_PATH)


@task
def syncdb():
    with cd(PROJECT_DIR):
        run('%spython manage.py syncdb' % BIN_PATH)
        run('%spython manage.py migrate' % BIN_PATH)