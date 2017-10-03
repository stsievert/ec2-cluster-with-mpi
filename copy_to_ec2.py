import os
import subprocess

DNS = ['ec2-54-202-13-84.us-west-2.compute.amazonaws.com',
       'ec2-54-245-196-251.us-west-2.compute.amazonaws.com']

dir = 'pytorch-mpi'
key_file = os.environ['KEY_FILE']  # path to .pem file
command = "scp -i {key_file} {file} ec2-user@{dns}:~/{dir}"

for file in ['mpi*', 'host*']:
    for dns in DNS:
        run = command.format(file=file, key_file=key_file, dns=dns, dir=dir)
        print(run)
        r = os.system(run)
