sudo mkdir /mirror
echo "w0:/mirror    /mirror    nfs" | sudo tee -a /etc/fstab
sudo mount -a  # requires UDP and TCP ports 111 and 20149 to be open
