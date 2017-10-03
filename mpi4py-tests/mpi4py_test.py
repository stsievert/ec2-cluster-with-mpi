#!/usr/bin/env python

"""
sudo yum install -y mpich2 mpich2-devel mpich2-autoload mpich2-doc
#  sudo yum -y install openmpi openmpi-devel
pip install mpi4py

$ mpiexec -n 4 python mpi4py_test.py
"""

import os
import torch
from torch import Tensor
import numpy as np
import mpi4py
import time
from pprint import pprint
from mpi4py import MPI
import numpy.linalg as LA

import mpi_torch

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
print(f"rank = {rank}")

num_messages = 10
n = 10
np.random.seed(42)
messages = [{'size': np.random.choice(n) + 1,
             'tag': i} for i in range(num_messages)]

if rank == 0:
    for i, message in enumerate(messages):
        messages[i]['data'] = np.ones(message['size'], dtype='float32')
        messages[i]['data'] *= message['tag']

    for i, message in enumerate(messages):
        mpi_torch.isend(messages[i]['data'], tag=message['tag'],
                        dest=1-rank)

elif rank == 1:
    for i, message in enumerate(messages):
        messages[i]['data'] = np.empty(message['size'], dtype='float32')

    requests = [mpi_torch.irecv(messages[i]['data'], tag=message['tag'],
                                source=1-rank)
                for i, message in enumerate(messages)]

    mpi_torch.wait(requests)

    for message in messages:
        show = {k: v for k, v in message.items() if k != 'data'}
        show['data_mean'] = message['data'].mean()
        pprint(show)
