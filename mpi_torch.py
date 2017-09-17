from mpi4py import MPI
import numpy as np
import torch

comm = MPI.COMM_WORLD


def isend(data, tag=None, dest=None, send=comm.Isend):
    if not isinstance(tag, int):
        raise ValueError('Pass an integer tag (mpi4py supports ints only)')
    assert dest is not None, "Specicy a destination"
    assert tag is not None, "Specicy a tag"

    if isinstance(data, torch.FloatTensor):
        data = data.numpy()

    send(data, dest=dest, tag=tag)


def irecv(data, tag=None, source=None, recv=comm.Irecv):
    assert tag is not None, "Specify a tag"
    assert source is not None, "Specify a source"
    return recv(data, source=source, tag=tag)


def wait(requests):
    for r in requests:
        r.Wait()


def format_results(results):
    return [torch.Tensor(x) for x in results]

def wait(requests):
    MPI.Request.Waitall(requests)
