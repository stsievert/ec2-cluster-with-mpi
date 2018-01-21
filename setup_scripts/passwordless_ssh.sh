
# ssh-keygen  # (accept defaults)
echo "Creating backups with `mv`"
mkdir ~/.ssh/
mv ~/.ssh/id_rsa ~/.ssh/id_rsa.orig  # not really needed (">" used below)
mv ~/.ssh/id_rsa.pub ~/.ssh/id_rsa.pub.orig
echo "Writing SSH auth files"
cat scott-key-dim.pem > ~/.ssh/id_rsa
chmod 700 ~/.ssh/id_rsa
