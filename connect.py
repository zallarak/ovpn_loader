#!/usr/bin/env python3

import os
import sys
import subprocess

USAGE = """
usage: python3 connect.py <user> <absolute path to ovpn file>

IMPORTANT: make sure you added the following line to your ovpn file:
auth-user-pass <absolute path to directory containing ovpn file>/creds.txt
"""
if sys.argv[1] == '--help':
    sys.exit(USAGE)
USER, OVPN_FILE_PATH = sys.argv[1], sys.argv[2]
BASE_DIR = os.path.dirname(OVPN_FILE_PATH)

if not os.path.exists(OVPN_FILE_PATH):
    print(USAGE)
    sys.exit('error: could not ovpn file: {}'.format(OVPN_FILE_PATH))

try:
    with open(BASE_DIR + 'creds.txt', 'w') as fh:
        data = fh.readlines()
except:
    data = []

auth = subprocess.check_output(
    'oathtool --base32 --totp {}'.format(
        os.environ.get('TOTP_CODE')).split()) # Replace env var where necessary

# username
if len(data) == 0: data.append(USER)
data[0] = USER

# pw
if len(data) == 1:
    data.append('')
data[1] = auth.strip().decode("utf-8") 

with open(BASE_DIR + 'creds.txt', 'w') as fh:
    fh.writelines('\n'.join(data))

subprocess.call('sudo openvpn {}'.format(OVPN_FILE_PATH).split())
