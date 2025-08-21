#!/usr/bin/env python3
'''A simple tool for uploading files to or downloading files from kDrive.'''

import argparse
import hashlib
import json
import pathlib
import sys
import urllib.request
import urllib.parse

ROOT = 1

def list_files(token:str, drive_id:int, parent:int) -> dict[str,int]:
    url = f'https://api.infomaniak.com/3/drive/{drive_id}/files/{parent}/files'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as reply:
        response_body = reply.read()
    j = json.loads(response_body)
    return { f['name']: int(f['id']) for f in j['data'] }


def get_file(token:str, drive_id:int, file_id:int) -> bytes:
    url = f'https://api.infomaniak.com/2/drive/{drive_id}/files/{file_id}/download'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as reply:
        return reply.read()


def put_file(token:str, drive_id:int, directory_id:int, src:pathlib.Path) -> str:
    size = src.stat().st_size
    contents = src.read_bytes()
    m = hashlib.sha256()
    m.update(contents)
    digest = m.hexdigest()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/octet-stream',
    }
    query = urllib.parse.urlencode({
        'conflict': 'error',
        'directory_id': directory_id,
        'file_name': src.name,
        'total_size': size,
        'total_chunk_hash': f'{m.name}:{digest}',
        'chunk_number': 1,
        'chunk_size': size,
    })
    url = f'https://api.infomaniak.com/3/drive/{drive_id}/upload?{query}'
    req = urllib.request.Request(url, headers=headers, data=contents)
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')


def download(token:str, drive_id:int, name:str) -> None:
    files = list_files(token, drive_id, ROOT)
    private = list_files(token, drive_id, files['Private'])
    data = get_file(token, drive_id, private[name])
    sys.stdout.buffer.write(data)


def upload(token:str, drive_id:int, src:pathlib.Path) -> None:
    files = list_files(token, drive_id, ROOT)
    response = put_file(token, drive_id, files['Private'], src)
    print(response)


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Up/Downloads a named file to/from kDrive')
    parser.add_argument('--token', type=str, help='An authorization token')
    parser.add_argument('--drive-id', type=int, help='kDrive id number')
    parser.add_argument('method',
                        choices=['put', 'get'],
                        help='Mode: put (upload) or get (download)')
    parser.add_argument('name', type=str,
                        help='The name of the file to be downloaded or the path to the uploaded')

    args = parser.parse_args()
    if args.method == 'put':
        upload(args.token, args.drive_id, pathlib.Path(args.name))
    else:
        download(args.token, args.drive_id, args.name)
    return 0

if __name__ == '__main__':
    sys.exit(main())
