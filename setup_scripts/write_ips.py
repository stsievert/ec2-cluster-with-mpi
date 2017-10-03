# on all nodes, edit /etc/hosts to include IP addresses of other machines
# name each machine "worker1" or something, and always associate one IP with
# worker1. Do this on all nodes with all IP addresses.

workers = {'w0': '172.31.19.203',
           'w1': '172.31.30.13'}

with open('/etc/hosts', 'ar') as f:
    for k, v in workers.items():
        if v in f.read():
            continue
        f.write('{k} {v}\n'.format(k=k, v=v))
