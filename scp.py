import subprocess

DNSs = ['ec2-54-202-19-126.us-west-2.compute.amazonaws.com',
        'ec2-54-187-124-161.us-west-2.compute.amazonaws.com',
        'ec2-54-191-13-106.us-west-2.compute.amazonaws.com',
        'ec2-34-213-223-151.us-west-2.compute.amazonaws.com',
        'ec2-54-149-46-238.us-west-2.compute.amazonaws.com']

key_file = '/Users/scott/Work/Developer/AWS/scott-key-dim.pem'

for dir in ['setup_scripts', 'tests']:
    for dns in DNSs:
        cmd = 'scp -i {key_file} -r {dir} ec2-user@{dns}:~/'
        subprocess.call(cmd.format(dns=dns, key_file=key_file, dir=dir).split(' '))
