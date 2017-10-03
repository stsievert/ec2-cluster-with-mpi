from mpi4py import MPI
import time
import numpy

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# automatic MPI datatype discovery
if rank == 0:
    for i in range(10):
        data = numpy.ones(10, dtype=numpy.float64) * i
        comm.Isend(data, dest=1, tag=i)

elif rank == 1:
    data = []
    for i in range(10):
        data += [numpy.empty(10, dtype=numpy.float64)]
    requests = []
    for i in range(10):
        requests += [comm.Irecv(data[i], source=0, tag=i)]
    for r in requests:
        r.Wait()
    print(data)
