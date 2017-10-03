sudo bash install_deps.sh
sudo python write_ips.py

# Start NFS
sudo chkconfig nfs on
sudo service rpcbind start
sudo service nfs start

sudo mkdir /mirror
master = 1
if [ $master == 1 ]
then
    bash master.sh
elif [ $master == 0 ]
then
    bash workers.sh
fi

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
