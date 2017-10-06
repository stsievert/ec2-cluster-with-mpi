import torch.distributed as dist
import torch

dist.init_process_group(backend='mpi')

rank = dist.get_rank()
world_size = dist.get_world_size()

print(f"Processor {rank} out of {world_size}")
