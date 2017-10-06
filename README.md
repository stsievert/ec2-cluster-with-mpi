
## Setup
All files except `scp.py` are in `setup_scripts`

### Local machine:
* copy Amazon EC2 key files (e.g., `scott-key-dim.pem`) to this folder
* include hosts files with private IPs in this directory (e.g., `hosts_file`)
* use `scp.py` to move this folder to EC2 domains (and modify the domains too)

### Remote machine
On every remote machine

* run `sudo bash main.sh`

### Security groups
MPI needs to have certain ports open for communication, and EC2 has security
groups to control this.

I opened ports 1-65535 to only the IPs of my cluster by

1. Creating one security group that opened port 22 to all IPs (which allows
   SSH).
    * This security group had a security group ID of `sg-xxxxxxxx`.
2. Creating another security group with custom UDP and TCP rules that opened
   ports 1-65535.
    * In this, I set the "Source" to `sg-xxxxxxxx`. This only allows access to
      the IPs that have security group `sg-xxxxxxxx`.

## Running
* To run MPI programs, use `mpiexec -n 3 -f hosts_file python [script].py`

## Notes
* Can SSH with private IPs (e.g., `ssh ec2-user@172.31.19.203` works).
* Useful wiki post on getting passwordless SSH setup
    * https://wiki.mpich.org/mpich/index.php/Using_MPICH_in_Amazon_EC2
* I launch with
    * AMI: ami-ceb545b6 anaconda-cuda-jupyter. It's a variant of Amazon's Deep
      Learning AMI
    * Security group: sg-f2937f8f jupyter+ssh+ports{3141,6282}

This is the command I'm using on 2017-10-06:

    mpiexec -n 2 -hostfile hosts_file python mpi4py_test.py -mca orte_base_help_aggregate 0


