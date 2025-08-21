#!/usr/bin/env python3

import os
import pathlib
import sys

import ktransfer

def main():
    print()
    print('->', os.environ)
    exit_code = 0
    token = os.getenv('PLUGIN_TOKEN')
    drive_id = int(os.getenv('PLUGIN_DRIVE_ID'))
    name = os.getenv('PLUGIN_NAME')
    method = os.getenv('PLUGIN_METHOD').lower()

    if method == 'put':
        ktransfer.upload(token, drive_id, pathlib.Path(name))
    elif method == 'get':
        ktransfer.download(token, drive_id, name)
    else:
        exit_code = 1
    return exit_code

if __name__ == '__main__':
    sys.exit(main())
