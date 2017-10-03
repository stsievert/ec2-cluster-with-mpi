# create NFS directory
echo "/mirror *(rw,sync)" | sudo tee -a /etc/exports
# restart NSF
sudo service nfs restart
