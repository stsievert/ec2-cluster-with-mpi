
## Passwordless login
ssh-keygen  # (accept defaults)
mv ~/.ssh/id_rsa ~/.ssh/id_rsa.orig  # not really needed (">" used below)
mv ~/.ssh/id_rsa.pub ~/.ssh/id_rsa.pub.orig
cat scott-key-dim.pem > ~/.ssh/id_rsa
