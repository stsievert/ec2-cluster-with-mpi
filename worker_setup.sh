
# install MPI
sudo yum install -y mpich2 mpich2-devel mpich2-autoload mpich2-doc
pip install mpi4py

# on all nodes, edit /etc/hosts to include IP addresses of other machines
# name each machine "worker1" or something, and always associate one IP with
# worker1. Do this on all nodes with all IP addresses.

sudo yum install -y openssh-server openssh-client
sudo yum install -y nfs-utils nfs-utils-lib

# Start NFS
sudo chkconfig nfs on
sudo service rpcbind start
sudo service nfs start

# XXX: begin ON MASTER NODE
# create NFS directory
sudo mkdir /mirror
echo "/mirror *(rw,sync)" | sudo tee -a /etc/exports
# restart NSF
sudo service nfs restart
### XXX: end ON MASTER NODE

### XXX: begin ON WORKER NODE
# on each of the other nodes (this one is named w1)
sudo mkdir /mirror

# edit /etc/fstab to include
w0:/mirror    /mirror    nfs

sudo mount -a  # requires UDP and TCP ports 111 and 20149 to be open
### XXX: end ON WORKER NODE

# Define a user to own /mirror (mpiu for mpiuser)
sudo adduser mpiu
sudo chown mpiu /mirror
# set up mpi to be sudoer
sudo passwd mpiu
# enter "this"
sudo visudo
mpiu ALL=(ALL) ALL  # add line at end of file

## Set up passwordless SSH
ssh-keygen -t rsa  # enter passphrase
cd .ssh
cat id_rsa.pub >> authorized_keys
