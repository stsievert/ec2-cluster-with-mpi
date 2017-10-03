from mpi4py import MPI
import time
import numpy

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# pass explicit MPI datatypes
#  if rank == 0:
   #  data = numpy.arange(1000, dtype='i')
   #  comm.Send([data, MPI.INT], dest=1, tag=77)
#  elif rank == 1:
   #  data = numpy.empty(1000, dtype='i')
   #  comm.Recv([data, MPI.INT], source=0, tag=77)

# automatic MPI datatype discovery
if rank == 0:
   data = numpy.ones(100, dtype=numpy.float64) * 42
   comm.Isend(data, dest=1, tag=13)

elif rank == 1:
   data = numpy.empty(100, dtype=numpy.float64)
   r = comm.Irecv(data, source=0, tag=13)
   r.Wait()
   print(data)
