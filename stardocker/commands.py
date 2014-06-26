import os
import stardocker.config
import stardocker.settings

def print_and_run(cmd):
    print cmd
    return os.popen(cmd).read()

def register_cluster(cluster_name, containers, volumes, nnodes, instance_type):
    config = stardocker.config.load()
    print 'Registering containers'
    config.set_containers(cluster_name, containers)
    print 'Registering volumes'
    config.set_volumes(cluster_name, volumes)
    print 'Setting size and instance type'
    config.set_size(cluster_name, nnodes)
    config.set_instance_type(cluster_name, instance_type)
    stardocker.config.save(config)

def _prepare_run_files(container, volumes, subdirs):
    container_dirname = container.replace('/','_')
    volumes_str = ' -v '.join(volumes)
    if not os.path.exists(container_dirname):
        os.mkdir(container_dirname)
    for sdir in subdirs:
        run_file = open(container_dirname + '/%s.sh' % sdir.replace('/', ''), 'w')
        run_file.write('docker run -v %s %s execute\n' % (volumes_str, container))
        run_file.close()
    return container_dirname

def run(name):
    print 'Attempting to run worker files on cluster'
    print_and_run('starcluster sshmaster %s "for i in `ls workers/`; do qsub $i; done"')
    print 'Cluster %s is now running' % (name)

def initialize_cluster(name, container, volumes, nnodes, instance_type):
    subdirs = []
    print 'Initializing cluster with configurations for container %s and volumes %s' % (container, volumes)
    print 'Registering cluster'
    register_cluster(name, [container], volumes, nnodes, instance_type)
    print 'Starting cluster'
    print_and_run('starcluster start %s' % name)
    print 'Getting volume information for /data/ volume from cluster'
    out = print_and_run('starcluster sshmaster %s "ls /data/"' % name)
    for l in out.split():
        subdirs.append(l)
    print 'Preparing container worker files'
    run_files_dir = _prepare_run_files(container, volumes, subdirs)
    print 'Sending worker files to cluster'
    print_and_run('starcluster put %s %s workers/' % (name, run_files_dir))
    f =  open(stardocker.settings.CONFIG_DIR + '%s_init' % name, 'a')
    f.close()
    print 'Finished initializing cluster'

def terminate_cluster(name):
    print 'Terminating cluster %s' % name
    print_and_run('starcluster terminate %s' % name)
    os.remove(stardocker.settings.CONFIG_DIR + '%s_init' % name)

def check_cluster_init(cluster_name):
    return os.path.exists(stardocker.settings.CONFIG_DIR + '%s_init' % name)
