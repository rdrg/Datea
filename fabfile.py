#!/usr/bin/env python
from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm
import os

# glogal env
env.warn_only = True
env.supervisor = '/etc/supervisord'
env.apache = '/etc/nginx/sites-enabled'

def clean():
    local("find . -name '*.DS_Store' -type f -delete")
    local("find . -name '*.pyc' -type f -delete")

def tx_push():
    """
    push translations
    """
    local('cd website && ./manage.py makemessages --all --ignore=socialregistration/* --ignore=filer/*')
    local('tx push -t -s') 

def tx_pull():
    """
    push translations
    """
    local('tx pull')
    local('cd website && ./manage.py compilemessages')
    
def acceso_datea_pe():
    env.site_id = 'acceso.datea.pe'
    env.hosts = ['acceso.datea.pe']
    env.git_url = 'https://github.com/rdrg/Datea.git'
    env.git_branch = 'stage'
    env.path = '/var/www/stage.artandthecity.ch'
    env.storage = '/var/www_data/stage.artandthecity.ch'
    env.user = 'root'