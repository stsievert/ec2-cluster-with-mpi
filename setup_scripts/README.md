
## Setup
* Local machine:
  * copy Amazon EC2 key files (e.g., `scott-key-dim.pem`) to this folder
  * include hosts files with private IPs in this directory (e.g., `hosts_file`)
  * use `scp.py` to move this folder to EC2 domains
* On every remote machine:
  * run `sudo bash main.sh`
  * To run MPI programs, use `mpiexec -n 3 -f hosts_file python my_script.py`

## Notes
* Can SSH with private IPs (e.g., `ssh ec2-user@172.31.19.203` works).
* Useful wiki post on getting passwordless SSH setup
    * https://wiki.mpich.org/mpich/index.php/Using_MPICH_in_Amazon_EC2
