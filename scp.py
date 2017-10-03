import subprocess

DNSs = ['ec2-54-190-37-5.us-west-2.compute.amazonaws.com',
        'ec2-34-213-5-153.us-west-2.compute.amazonaws.com']

key_file = '/Users/scott/Work/Developer/AWS/scott-key-dim.pem'
for dns in DNSs:
    cmd = 'scp -i {key_file} -r setup_scripts ec2-user@{dns}:~'
    subprocess.call(cmd.format(dns=dns, key_file=key_file).split(' '))
