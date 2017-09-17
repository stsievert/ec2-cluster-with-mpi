from mpi4py import MPI
import numpy as np
import torch

comm = MPI.COMM_WORLD

def isend(data, tag=None, dest=None, blocking=False):
    if type(tag) is not int:
        raise ValueError('Pass an integer tag (mpi4py supports ints only)')
    assert dest is not None, "Specicy a destination"
    assert tag is not None, "Specicy a tag"

    if type(data) == torch.FloatTensor:
        data = data.numpy()

    if blocking:
        comm.send(data, dest=dest, tag=tag)
    else:
        comm.Isend(data, dest=dest, tag=tag)

def irecv(data, tag=None, source=None, blocking=False):
    assert tag is not None, "Specify a tag"
    assert source is not None, "Specify a source"
    if blocking:
        return comm.recv(data, source=source, tag=tag)
    return comm.Irecv(data, source=source, tag=tag)


def format_results(results, tags):
    return [torch.Tensor(x) if tag < 0 else x
            for tag, x in zip(tags, results)]

def wait(requests):
    MPI.Request.Waitall(requests)
