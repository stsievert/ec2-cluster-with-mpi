import subprocess

DNSs = ['ec2-54-244-76-187.us-west-2.compute.amazonaws.com',
        'ec2-34-209-85-116.us-west-2.compute.amazonaws.com']

key_file = '/Users/scott/Work/Developer/AWS/scott-key-dim.pem'
for dns in DNSs:
    cmd = 'scp -i {key_file} -r . ec2-user@{dns}:~/setup_scripts'
    subprocess.call(cmd.format(dns=dns, key_file=key_file).split(' '))
