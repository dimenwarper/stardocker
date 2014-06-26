from setuptools import setup
import sys
import os

setup(name='stardocker',
        version='0.1',
        description='Flexible framework based on starcluster to run docker containers in the Amazon AWS with minimal effort',
        author='Pablo Cordero',
        author_email='dimenwarper@gmail.com',
        packages=['stardocker'],
        install_requires=['StarCluster']
        )

if sys.argv[-1] == 'install':
    print 'Installing scripts'
    os.system('mkdir ~/.stardocker')
    os.system('chmod a+w ~/.stardocker')
    os.system('echo "#!%s" > /usr/bin/stardocker' % sys.executable)
    os.system('cat bin/stardocker.py >> /usr/bin/stardocker')
    os.system('chmod a+x /usr/bin/stardocker')
    print 'Installing starcluster plugins'
    os.system('cp stardocker/stardocker_plugin.py ~/.starcluster/plugins/.')
