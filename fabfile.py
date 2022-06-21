# -*- coding: utf-8 -*-

from datetime import datetime
from fabric.api import *

MODULE_TAR_FILE = 'easy_http.tar.gz'

env.user = 'work'
env.hosts = ['10.33.108.27']

tag = datetime.now().strftime('%y.%m.%d_%H.%M.%S')
remote_dist_dir = '/data0/easy_http/easy_http_%s' % tag


def pack():
    tar_files = ['*.py', '*.sh', '*.txt', 'agent/*', 'alert/*', 'api/*', 'dash/*', 'schedule/*', 'task/*', 'utils/*', 'bin/*']
    local('rm -f %s' % MODULE_TAR_FILE)
    local('tar -czvf easy_http.tar.gz --exclude=\'*.tar.gz\' --exclude=\'fabfile.py\' %s' % ' '.join(tar_files))


def deploy():
    remote_tmp_dir = '/data0/tmp/'
    remote_tmp_tar = remote_tmp_dir + MODULE_TAR_FILE
    run('rm -f %s' % remote_tmp_tar)
    run('mkdir -p %s' % remote_tmp_dir)
    put(MODULE_TAR_FILE, remote_tmp_tar)
    run('mkdir -p %s' % remote_dist_dir)
    with cd(remote_dist_dir):
        run('tar -xzvf %s' % remote_tmp_tar)
        sudo('pip install -r requirements.txt')


def deploy_server():
    env.hosts = ['10.33.108.27']
    env.passwords = {
        'work@10.33.108.27:22': 'rent@2017',
    }
    deploy()
    with cd(remote_dist_dir):
        run('sh run_server.sh fstop')
        run('sh run_server.sh start && sleep 2')
