#!/usr/bin/python2

import argparse
import os.path
import socket
try:
    from jnpr.junos import Device
except ImportError:
    raise ImportError('jnpr.junos python library not installed! Please install the library:  pip install junos-eznc')

# definition of Constants
EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3

# define arguments to programm
parser = argparse.ArgumentParser(description='check root-fs of juniper srx boxes')
parser.add_argument('-H', dest='host', help='ip-address or hostname of srx-box to connect to', required=True)
parser.add_argument('-u', dest='user', help='username to connecto to the srx-box', required=True)
parser.add_argument('-p', dest='passwd', help='password to connecto to the srx-box')
parser.add_argument('-k', dest='ssh_key_file', help='path to ssh-key-file for connection to srx-box')
args = parser.parse_args()

# try to read ssh_key_file if parameter was set
if args.ssh_key_file is not None:
  print 'ssh_key_file', args.ssh_key_file
  if not os.path.isfile(args.ssh_key_file):
    raise ValueError('ssh-key-file dont exists or is not readable')

# try to resolve hostname / ip-adress
socket.gethostbyname(args.host)

# try to reach juniper srx box
dev = Device(host=args.host, user=args.user, password=args.passwd )
dev.open()
bp = dev.rpc.get_system_storage_partitions()
partition = bp.findtext('.//partitions/booted-from').strip()
if partition == 'active':
  print 'OK - srx booted from active boot partition'
  raise SystemExit, EXIT_OK
print('CRITICAL - srx booted from ' + partition + ' partition')
raise SystemExit, EXIT_CRITICAL
