from fabric.api import *
from fabric.contrib.project import rsync_project


env.hosts = ['jamie@jdpaton.com']


def pack():
    from datetime import datetime
    local('tar czf /tmp/urly%s.tgz .' % datetime.strftime(datetime.today(), "-%d%m%y_%H:%M"), capture=False)

def deploy():
  rsync_project(remote_dir='/var/www/html/', exclude= ('settings.py', 'urly.wsgi', 'db') )
  run('cd /var/www/html/urly')
  #run('chown -R apache:apache *')
  run('touch urly.wsgi')
