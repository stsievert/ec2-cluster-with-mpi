import subprocess

DNSs = ['ec2-54-191-123-251.us-west-2.compute.amazonaws.com',
        'ec2-34-213-224-63.us-west-2.compute.amazonaws.com',
        'ec2-34-215-180-57.us-west-2.compute.amazonaws.com']

key_file = '/Users/scott/Work/Developer/AWS/scott-key-dim.pem'

for dir in ['setup_scripts', 'tests']:
    for dns in DNSs:
        cmd = 'scp -i {key_file} -r {dir} ec2-user@{dns}:~/'
        subprocess.call(cmd.format(dns=dns, key_file=key_file, dir=dir).split(' '))
