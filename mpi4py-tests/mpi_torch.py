from mpi4py import MPI
import numpy as np
import torch

comm = MPI.COMM_WORLD


def isend(data, tag=None, dest=None, send=comm.Isend):
    """
    Parameters
    ----------
    data : np.ndarray, torch.Tensor
        Data to send
    tag : int
        Message identifier
    dest : int
        Machine to send to
    send : callable, str
        The function to call (from mpi4py.MPI.COMM_WORLD)

    Returns
    -------
    The return value of `send`

    """
    if isinstance(send, str):
        send = getattr(comm, send)
    if not isinstance(tag, int):
        raise ValueError('Pass an integer tag (mpi4py supports ints only)')
    assert dest is not None, "Specicy a destination"
    assert tag is not None, "Specicy a tag"

    if isinstance(data, torch.FloatTensor):
        data = data.numpy()

    return send(data, dest=dest, tag=tag)


def irecv(data, tag=None, source=None, recv=comm.Irecv):
    """
    Parameters
    ----------
    data : np.ndarray, torch.Tensor
        Data to send
    tag : int
        Message identifier
    source : int
        Machine to receive from
    recv : callable, str
        The function to call (from mpi4py.MPI.COMM_WORLD)

    Returns
    -------
    The return value of `recv`

    """
    if isinstance(recv, str):
        recv = getattr(comm, recv)
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
