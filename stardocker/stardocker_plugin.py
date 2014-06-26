import stardocker.config
from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log


class StarDockerInstaller(ClusterSetup):
    def __init__(self, containers, volumes):
        self.containers = [c.strip() for c in containers.split(',')]
        self.volumes = [stardocker.config.Volume(v.strip()) for v in volumes.split(',')]
    
    def base_dependencies(self, node):
        node.ssh.execute('sudo apt-get -y update')
        node.ssh.execute('sudo apt-get -y install linux-image-extra-`uname -r`')
        node.ssh.execute('sudo sh -c "curl https://get.docker.io/gpg | apt-key add -"')
        node.ssh.execute('sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9')
        node.ssh.execute('sudo sh -c "echo deb http://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"')
        node.ssh.execute('sudo apt-get -y update')
        node.ssh.execute('sudo apt-get -y install lxc-docker')
        node.ssh.execute('sudo apt-get -y install python-pip')
        node.ssh.execute('sudo pip install awscli')

    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes + [master]:
            log.info('Installing base dependencies on %s' % node.alias)
            self.base_dependencies(node)
            
        log.info('Pulling docker containers')
        for container in self.containers:
            master.ssh.execute('docker pull %s' % container)

        for volume in self.volumes:
            if volume.type == 's3':
                master.ssh.execute('aws s3 sync %s %s' % (volume.origin, volume.local))


