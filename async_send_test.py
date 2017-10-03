import os
import numpy as np
from pprint import pprint
import time

import torch
import torch.distributed as dist
import torch.nn as nn
from torchvision import datasets, transforms
from torch.autograd import Variable
import torch.nn.functional as F
import torch.optim as optim

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x)

def _set_up_distributed(url='127.0.0.1', port=3255, world_size=2):
    if 'RANK' not in os.environ:
        raise ValueError('`RANK` is not in enviroment variables')
    local_rank = int(os.environ['RANK'])
    dist.init_process_group(backend='tcp', init_method=f'tcp://{url}:{port}',
                            world_size=world_size, rank=local_rank)

    my_rank = torch.distributed.get_rank()
    num_processes = torch.distributed.get_world_size()
    return {'local': my_rank, 'num_processes': num_processes}

print('Setting up distributed...')
dist_info = _set_up_distributed()
#  dist_info = {'local': 0, 'num_processes': 2}
assert dist_info['num_processes'] == 2
dist_info['remote'] = 1 - dist_info['local']
pprint(dist_info)

model = Net()
params = [{'name': k, 'shape': v.size(), 'total_size': np.prod(v.size())}
              for k, v in model.state_dict().items()]

params[0]['start'] = 0
for i in range(len(params)):
    if i == 0:
        continue
    params[i]['start'] = params[i - 1]['total_size'] + params[i - 1]['start']

total_params = int(sum(p['total_size'] for p in params))


message = [v.numpy().flat[:] for k, v in model.state_dict().items()]
message = np.concatenate(message)
message = torch.Tensor(message)
if dist_info['local'] == 0:
    dist.send(message, dist_info['remote'])
    print(message)

elif dist_info['local'] == 1:
    message_hat = torch.Tensor(total_params)
    dist.recv(message_hat, dist_info['remote'])
    print(message_hat)
    values = message_hat.numpy()
    print(np.allclose(values, message.numpy()))
    error = np.abs(values - message.numpy())
    print(error.max(), error.mean(), np.median(error))

    state = {}
    for param in params:
        value = values[param['start']:param['start'] + param['total_size']]
        value = value.reshape(param['shape'])
        state[param['name']] = torch.Tensor(value)

    #  pprint(params_)
    error = {k: v1 - v2 for (k, v1), (k, v2) in
             zip(model.state_dict().items(), state.items())}
    #  print(error)
