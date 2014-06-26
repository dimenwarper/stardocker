from stardocker import settings
import pdb

class Volume(object):
    def __init__(self, vol_str):
        if vol_str.count(':') > 1:
            self.type, self.origin, self.local = vol_str.split(':')
            self.origin = self.origin.replace('//','')
        else:
            self.origin, self.local = vol_str.split(':')
            self.type = 'local'

    def __str__(self):
        if self.type == 'local':
            return '%s:%s' % (self.origin, self.local)
        else:
            return '%s://%s:%s' % (self.type, self.origin, self.local)


class StarDockerCluster(object):
    def __init__(self):
        self.containers = []
        self.volumes = []
        self.size = 5
        self.instance_type = 'm1.small'

    def __str__(self):
        return 'Cluster with %s nodes, instance type %s, containers %s, and volumes %s' % (self.size, self.instance_type, self.containers, [str(v) for v in self.volumes])

class StarClusterConfigHandler(object):
    def __init__(self):
        self.clusters = {}

    def load(self, configfile):
        parse = False
        for line in configfile:
            if '[stardocker]' in line:
                parse = True
            if parse:
                if '[' in line:
                    curr_section = line.strip().replace('[','').replace(']', '').split()
                else:
                    if curr_section[0] == 'plugin':
                        cname = curr_section[1].replace('_plugin', '').strip()
                        if cname not in self.clusters:
                            self.clusters[cname] = StarDockerCluster()
                        if 'volumes' in line:
                            vols_str = line.replace('volumes=', '')
                            for vol_str in vols_str.split(','): 
                                self.clusters[cname].volumes.append(Volume(vol_str.strip()))
                        if 'containers' in line:
                            containers_str = line.replace('containers=', '')
                            for con_str in containers_str.split(','):
                                self.clusters[cname].containers.append(con_str.strip())
                    if curr_section[1] == 'cluster':
                        cname = curr_section[1].strip()
                        if 'CLUSTER_SIZE' in line:
                            self.clusters[cname].size = int(line.replace('CLUSTER_SIZE=',''))
                        if 'NODE_INSTANCE_TYPE' in line:
                            self.clusters[cname].instance_type = line.replace('NODE_INSTANCE_TYPE=','')

    def add_container(self, cluster_name, container):
        if cluster_name not in self.clusters:
            self.clusters[cluster_name] = StarDockerCluster()
        self.clusters[cluster_name].containers.append(container)

    def add_volume(self, cluster_name, vol_str):
        if cluster_name not in self.clusters:
            self.clusters[cluster_name] = StarDockerCluster()
        self.clusters[cluster_name].volumes.append(Volume(vol_str))

    def set_containers(self, cluster_name, containers):
        if cluster_name not in self.clusters:
            self.clusters[cluster_name] = StarDockerCluster()
        self.clusters[cluster_name].containers = containers

    def set_volumes(self, cluster_name, vol_strs):
        if cluster_name not in self.clusters:
            self.clusters[cluster_name] = StarDockerCluster()
        self.clusters[cluster_name].volumes = [(Volume(v)) for v in vol_strs]

    def set_size(self, cluster_name, nnodes):
        if cluster_name not in self.clusters:
            self.clusters[cluster_name] = StarDockerCluster()
        self.clusters[cluster_name].size = nnodes

    def set_instance_type(self, cluster_name, instance_type):
        if cluster_name not in self.clusters:
            self.clusters[cluster_name] = StarDockerCluster()
        self.clusters[cluster_name].instance_type = instance_type

    def __str__(self):
        out_str = '''
##############################
## StarDocker configuration ##
##############################
# Don't alter this section manually! Use stardocker utilities instead
# [stardocker]
        '''
        for cname, cluster in self.clusters.iteritems():
            out_str += '\n[plugin %s_plugin]\n' % cname
            out_str += 'setup_class=stardocker_plugin.StarDockerInstaller\n'
            out_str += 'containers=%s\n' % ','.join([str(c) for c in cluster.containers])
            out_str += 'volumes=%s\n' % ','.join([str(v) for v in cluster.volumes])
            out_str += '\n[cluster %s]\n' % cname
            #TODO make own extensible cluster entry
            out_str += 'EXTENDS=smallcluster\n'
            out_str += 'CLUSTER_SIZE=%s\n' % cluster.size
            out_str += 'NODE_INSTANCE_TYPE=%s\n' % cluster.instance_type
            out_str += 'plugins=%s_plugin\n' % cname
        return out_str


def load():
    config = StarClusterConfigHandler()
    config.load(open(settings.STARCLUSTER_CONFIG))
    return config

def get_starcluster_config_lines():
    config_file = open(settings.STARCLUSTER_CONFIG)
    lines = []
    for line in config_file:
        if 'StarDocker' in line:
            break
        lines.append(line)
    return lines[:-1]

def save(config):
    prev_lines = get_starcluster_config_lines()
    config_file = open(settings.STARCLUSTER_CONFIG, 'w')
    for line in prev_lines:
        config_file.write(line)
    config_file.write(str(config))
    config_file.close()
    
