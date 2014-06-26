import argparse
import stardocker.commands

if __name__ == '__main__':
    parser = argparse = argparse.ArgumentParser()
    parser.add_argument('command', type=str)
    parser.add_argument('cluster_name', type=str)
    parser.add_argument('--container', type=str, default='')
    parser.add_argument('--volumes', type=str, nargs='+', default=[])
    parser.add_argument('--nnodes', type=int, default=5)
    parser.add_argument('--instance_type', type=str, default='m1.small')

    args = parser.parse_args()

    if args.command == 'up':
        if len(args.container) == 0:
            print 'ERROR: Need to specify a container with the --container option!'

        if len(args.volumes) == 0:
            print 'ERROR: Need to specify at leas one volume with the --volumes option!'
        stardocker.commands.initialize_cluster(args.cluster_name, args.container, args.volumes, args.nnodes, args.instance_type)
    
    if args.command == 'run':
        if not stardocker.commands.check_cluster_init(args.cluster_name):
            print 'Cluster %s is not initialized, us stardocker up command to initialize it' % args.cluster_name
        else:
            stardocker.commands.run(args.cluster_name)
    if args.command == 'terminate':
        stardocker.commands.terminate(args.cluster_name)

