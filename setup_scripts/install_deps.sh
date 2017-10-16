# install MPI
sudo yum install -y mpich mpich-devel mpich-autoload mpich-doc

# make sure SSH installed
sudo yum install -y openssh-server openssh-client

# `sudo pip != ancaond pip`!
/home/ec2-user/anaconda3/bin/pip install mpi4py
