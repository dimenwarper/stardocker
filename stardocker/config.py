from stardocker import settings


class Volume(object):
    def __init__(self, *args):
        self.local, self.origin, self.type = args

    def __str__(self):
        return 'Volume: cluster url %s; origin url %s; type %s' % (self.local, self.origin, self.type)

class StarClusterPluginConfig(object):
    def __init__(self):
        self.containers = []
        self.volumes = {}

    def load(self, configfile):
        for line in configfile:
            fields = line.strip().split('\t')
            if 'CONTAINER' in line:
                self.containers.append(fields[1])
            if 'VOLUME' in line:
                self.volumes.append(Volume(*fields))

    def add_container(self, container):
        self.container.append(container)

    def add_volume(self, origin, local, type):
        self.volumes.append(Volume(origin, local, type))


    def __str__(self):
        out_str = ''
        for container in self.containers:
            out_str += 'CONTAINER\t%s\n' % container
        for volume in self.volumes:
            out_str += 'VOLUME\t%s\t%s\t%s\n' % (volume.local, volume.origin, volume.type)
        return out_str

    def to_python(self):
        python_str = ''
        python_str += 'from starcluster.clustersetup import ClusterSetup\n'
        python_str += 'from starcluster.logging import log\n'
        python_str += '    class StarDockerInstaller(ClusterSetup):\n'
        python_str += '        def __init__(self):\n'
        python_str += '            pass\n'
        python_str += '        def base_dependencies(self, node):\n'
        python_str += '            node.ssh.execute("sudo apt-get -y update")\n'
        python_str += '            node.ssh.execute("sudo apt-get -y install linux-image-extra-`uname -r`")\n'
        python_str += '            node.ssh.execute("sudo sh -c "curl https://get.docker.io/gpg | apt-key add -"")\n'
        python_str += '            node.ssh.execute("sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9")\n'
        python_str += '            node.ssh.execute("sudo sh -c \\"echo deb http://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list\\"")\n'
        python_str += '            node.ssh.execute("sudo apt-get -y update")\n'
        python_str += '            node.ssh.execute("sudo apt-get -y install lxc-docker")\n'
        python_str += '        def run(self, nodes, master, user, user_shell, volumes):\n'
        python_str += '            for node in nodes + [master]:\n'
        python_str += '                 log.info("Installing base dependencies on " % node.alias)\n'
        python_str += '                 self.base_dependencies(node)\n'

        for container in self.containers:
            python_str += '            master.ssh.execute("docker pull %s")\n' % container

        for volume in self.volumes:
            if volume.type == 's3':
                python_str += '            master.ssh.execute("aws s3 sync %s %s")\n' % (volume.origin, volume.local)


        return python_str


def load():
    config = StarClusterPluginConfig()
    config.load(open(settings.CONFIG))
    return config

def save(config):
    config_file = open(settings.CONFIG, 'w')
    config_file.write(str(config))
    config_file.close()
    starcluster_plugin_config = open('~/.starcluster/plugins/stardocker_config.py', 'w')
    starcluster_plugin_config.write(config.to_python())
    starcluster_plugin_config.close()
    
