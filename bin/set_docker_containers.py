#!/bin/python
import argparse
import stardocker.config


def set_docker_containers(containers):
    config = stardocker.config.load()
    for container in containers:
        config.add_container(container)
    stardocker.config.save(config)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('containers', type=str, nargs='+')
    args = parser.parse_args()
    set_docker_containers(args.containers)

