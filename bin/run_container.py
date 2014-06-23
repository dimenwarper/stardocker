#!/bin/python
import argparse
import os

def print_and_run(cmd):
    print cmd
    return os.popen(cmd).read()

def prepare_run_files(container, volumes, subdirs):
    container_dirname = container.replace('/','_')
    volumes_str = ' -v '.join(volumes)
    if not os.path.exists(container_dirname):
        os.mkdir(container_dirname)
    for sdir in subdirs:
        run_file = open(container_dirname + '/%s.sh' % sdir.replace('/', ''), 'w')
        run_file.write('docker run -v %s %s execute\n' % (volumes_str, container))
        run_file.close()
    return container_dirname

def run(container, volumes):
    subdirs = []
    container_dirname = container.replace('/','_')
    print 'Attempting to run container %s with volumes %s' % (container, volumes)
    print 'Starting cluster'
    print_and_run('starcluster stardocker start')
    print 'Getting volume information for /data/ volume from cluster'
    out = print_and_run('starcluster sshmaster "ls /data/"')
    for l in out.split():
        subdirs.append(l)
    print 'Preparing container worker files'
    run_files_dir = prepare_run_files(container, volumes, subdirs)
    print 'Sending worker files to cluster'
    print_and_run('starcluster put %s %s/' % (run_files_dir, container_dirname))
    print 'Attempting to run worker files on cluster'
    print_and_run('starcluster sshmaster "%s"' % ' && '.join(['sh %s' % fname for fname in os.listdir(run_files_dir)]))
    print 'Cluster is now running container %s with volumes %s' % (container, volumes)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('container', type=str)
    parser.add_argument('volumes', type=str, nargs='+', help='A series of volume strings of the form "local_dir:container_dir" that will be passed to the container as volume arguments. One of them is necessarily the data volume, i.e. /local/path/to/data/:/data/')
    """
    For future versions, right now we support only
    running a 'worker' docker that focuses on data
    in each subdirectory of the volume.
    We might want to support tasks where the docker
    submits its own qsub commands
    """
    #parser.add_argument('runtype', type=str)
    args = parser.parse_args()
    run(args.container, args.volumes)

