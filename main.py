import os
import sys
import json
import glob
import requests

def upload(url, param, filename):
    try:
        r = requests.post(url, files={
            param: open(filename, mode='rb'),
        })
    except:
        return

    if r.status_code == 200:
        try:
            print(url)
            print(r.json())
        except json.decoder.JSONDecodeError:
            return

def main():
    os.chdir('uploaders')
    for f in glob.glob('*.sxcu'):
        with open(f, mode='rb') as handle:
            try:
                # all the files have byte order mark for some reason
                # json library does not like this so we use special codec
                config = json.loads(handle.read().decode('utf-8-sig'))
            except:
                continue #there is one config with a trailing comma
        #print(config)

        if 'FileFormName' not in config:
            continue

        if 'RequestURL' not in config:
            continue

        upload(config['RequestURL'], config['FileFormName'], sys.argv[1])

if __name__ == '__main__':
    main()
