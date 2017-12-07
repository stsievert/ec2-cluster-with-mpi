# install MPI
# sudo yum install -y mpich mpich-devel mpich-autoload mpich-doc
sudo yum install -y openmpi openmpi-devel

# make sure SSH installed
sudo yum install -y openssh-server openssh-clients

# `sudo pip != ancaond pip`!
/home/ec2-user/anaconda3/bin/pip install mpi4py
/home/ec2-user/anaconda3/bin/pip install dask distributed --upgrade
