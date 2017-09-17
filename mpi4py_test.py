#!/usr/bin/env python

"""
sudo yum install -y mpich2 mpich2-devel mpich2-autoload mpich2-doc
#  sudo yum -y install openmpi openmpi-devel
pip install mpi4py

$ mpirun -np 4 python mpi4py_test.py
"""

import os
import torch
from torch import Tensor
import numpy as np
import mpi4py
import time
from mpi4py import MPI
import numpy.linalg as LA

import mpi_torch

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
print(f"rank = {rank}")

num_messages = 10
n = 10
np.random.seed(42)
sizes = np.random.choice(n, size=num_messages) + 1
sizes = np.ones(num_messages, dtype=int) * 300
print("messages are sized", sizes)

blocking = True
send_seq = {i: np.ones(size, dtype=np.float32) * i
            for i, size in enumerate(sizes)}
if rank == 0:
    for i, send in send_seq.items():
        mpi_torch.isend(send, tag=i, dest=1-rank, blocking=blocking)

elif rank == 1:
    recv_seq = {i: np.empty(size, dtype=np.float32)
                for i, size in enumerate(sizes)}
    requests = []
    for i in recv_seq:
        requests += [mpi_torch.irecv(recv_seq[i], tag=i, source=1-rank, blocking=blocking)]

    #  for r in requests:
        #  r.Wait()
    #  mpi_torch.wait(requests)
    time.sleep(2.5)

    for (sent_i, sent), (recv_i, recv) in zip(send_seq.items(), recv_seq.items()):
        #  sent = sent.numpy()
        #  rel_error = LA.norm(sent - recv) / (LA.norm(recv) + 1e-8)
        #  error = np.abs(sent - recv)
        print("-"*40)
        print(f"sent_i = {sent_i}, recv_i = {recv_i}")
        print(f"sent.mean = {sent.mean()}, recv.mean = {recv.mean()}")
        #  assert np.allclose(sent, recv)
