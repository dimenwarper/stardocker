#!/bin/python
import argparse
import stardocker.config


def set_bucket(bucket, local):
    config = stardocker.config.load()
    config.add_volume(bucket, local, 's3')
    stardocker.config.save(config)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bucket', type=str)
    parser.add_argument('local', type=str)
    args = parser.parse_args()
    set_bucket(args.bucket, args.local)

