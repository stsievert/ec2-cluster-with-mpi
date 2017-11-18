import os
import sys
import boto3
import pickle
from joblib import Parallel, delayed
from datetime import datetime
today = datetime.now().isoformat()[:10]

class EC2:
    def __init__(self, cfg):
        self.cfg = cfg

    def _get_cluster(self):
        filters = [{'Name': 'instance-state-name', 'Values': ['running']},
                   {'Name': 'key-name', 'Values': [self.cfg['key_name']]}]
        live_instances = ec2.instances.filter(Filters=filters)

        return live_instances

    def wait_until_initialized(self):
        instances = self._get_cluster()
        for instance in instances:
            instance.wait_until_running()


    def launch(self):
        tags = [{'Key': 'cluster-name', 'Value': self.cfg['cluster']['name']}]
        instance_type = self.cfg['instance_type']
        kwargs = {'MinCount': self.cfg['cluster']['count'],
                  'MaxCount': self.cfg['cluster']['count'],
                  'KeyName': self.cfg['key_name'],
                  'InstanceType': self.cfg['cluster']['instance_type'],
                  'ImageId': self.cfg['ami'],
                  'Placement': {'AvailabilityZone': self.cfg['availability_zone']},
                  'SecurityGroups': self.cfg['security_groups']}
        if instance_type == 'dedicated':
            r = client.run_instances(**kwargs)
        elif instance_type == 'spot-instance':
            count = kwargs.pop('MinCount')
            kwargs.pop('MaxCount')
            r = client.request_spot_instances(InstanceCount=count,
                                              LaunchSpecification=kwargs,
                                              SpotPrice=self.cfg["spot_price"])
        else:
            msg = 'cfg["instance_type"]=={instance_type} not one in {types]'
            raise ValueError(msg.format(types=['dedicated', 'spot-instance'],
                                        instance_type=instance_type))

        self.wait_until_initialized()
        return r

    def write_public_dnss(self, filename):
        instances = self._get_cluster()
        DNSs = [instance.public_dns_name for instance in instances]
        with open(filename, 'w') as f:
            print('\n'.join(DNSs), file=f)

    def write_private_ips(self, filename):
        instances = self._get_cluster()
        ips = [instance.private_ip_address for instance in instances]
        with open(filename, 'w') as f:
            print('\n'.join(ips), file=f)

    #  def scp_up(self, files='../WideResNet-pytorch/*.py ../WideResnet-pytorch/comms/*.py hosts ../WideResNet-pytorch/tools/run.py',
    def scp_up(self, files='../WideResNet-pytorch/* hosts',
               out='WideResNet-pytorch', flags=''):
        instances = self._get_cluster()
        ips = [instance.classic_address.public_ip for instance in instances]
        cmd = 'scp -i {key} {flags} {files} ec2-user@{ip}:~/{out}'
        for ip in ips:
            run = cmd.format(key=self.cfg['key_file'], files=files,
                             ip=ip, out=out, flags=flags)
            os.system(run)

    def run_cluster_ssh_command(self, cmd):
        instances = self._get_cluster()
        ips = [instance.classic_address.public_ip for instance in instances]
        to_run = 'ssh -i {keyfile} ec2-user@{ip} "{cmd}"'

        commands = [to_run.format(keyfile=self.cfg['key_file'], ip=ip, cmd=cmd)
                    for ip in ips]
        print('Running on every node in cluster:')
        print(commands[0])
        Parallel(n_jobs=len(commands))(delayed(os.system)(command)
                                       for command in commands)

    def run_command_one_node(self, cmd):
        instances = self._get_cluster()
        ips = [instance.classic_address.public_ip for instance in instances]
        ip = ips[0]
        to_run = 'ssh -i {keyfile} ec2-user@{ip} "{cmd}"'
        run = to_run.format(keyfile=self.cfg['key_file'], ip=ip, cmd=cmd)
        print(run)
        os.system(run)
        return ip

    def terminate(self):
        instances = self._get_cluster()
        ids = [x.id for x in instances]
        print(ids)
        if len(ids) != 0:
            print("Terminating instances: %s" %
                  (" ".join([str(x) for x in ids])))
            client.terminate_instances(InstanceIds=ids)


cfg = {'region': 'us-west-2', 'availability_zone': 'us-west-2b',
       'ami': 'ami-ceb545b6',
       #  'security_groups': ['sg-2d241757',  # Jupyter notebooks
                           #  'sg-f2937f8f',  # jupyter + ssh + ports{3141,6282}
                           #  'sg-491aa934',  # MPI1
                           #  'sg-ef1fac92'],  # MPI2
       'security_groups': ['Jupyter notebooks',
                           'jupyter+ssh+ports{3141,6282}',
                           'MPI1',
                           'MPI2'],
       'instance_type': 'spot-instance',
       'spot_price': '0.62',  # must be a str
       'key_name': 'scott-key-dim',
       'key_file': '/Users/scott/Work/Developer/AWS/scott-key-dim.pem',
       'cluster': {'count': 1, 'instance_type': 'p2.xlarge',
                   'name': 'scott-compress'},
       }
client = boto3.client("ec2", region_name=cfg['region'])
ec2 = boto3.resource("ec2", region_name=cfg['region'])

if __name__ == "__main__":
    # python launch.py --seed=42 --layers=62 --compress=1
    cloud = EC2(cfg)
    if len(sys.argv) < 2:
        print('Usage: python launch.py command [custom_cluster_command]')
        sys.exit(1)
    command = sys.argv[1]
    if command == 'launch':
        cluster = cloud.launch()
        print("Lauched, now waiting to enter ssh-ready state...")
        #  cloud.wait_until_initialized()  # doesn't work
    elif command == 'setup':
        cloud.write_public_dnss('DNSs')
        cloud.write_private_ips('hosts')
        cloud.scp_up()
        cloud.scp_up(files='./setup_scripts/', out='', flags='-r')
        cloud.run_cluster_ssh_command('cd setup_scripts; bash main.sh')
        cloud.run_cluster_ssh_command('ssh-keyscan -f ~/WideResNet-pytorch/hosts >> ~/.ssh/known_hosts')
    elif command in {'scp', 'scp_up'}:
        cloud.scp_up()
        cloud.run_cluster_ssh_command('mkdir /home/ec2-user/WideResNet-pytorch/comms')
        cloud.scp_up(files='../WideResNet-pytorch/comms/*.py',
                     out='WideResNet-pytorch/comms/')
    elif command == 'debug':
        cloud.run_cluster_ssh_command('killall python')
        cloud.scp_up()
        cloud.scp_up(files='../WideResNet-pytorch/comms/*.py',
                     out='WideResNet-pytorch/comms/')
    elif command in {'terminate', 'shutdown'}:
        cloud.terminate()
    elif command == 'custom':
        cmd = sys.argv[2]
        cloud.run_cluster_ssh_command(cmd)
    else:
        raise ValueError('Usage: python launch.py [command].\n'
                         '`command` not recognized.')
