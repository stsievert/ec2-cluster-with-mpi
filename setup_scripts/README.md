
It looks like I should be using Amazon EC2 private IPs: https://github.com/hwang595/pytorch_distributed_nn/blob/41be7dfc6719d2b4c9c1216035cd0126cf7dcecd/tools/hosts

I think Hongwai uses a tensorflow startup script for different EC2 machines? https://github.com/hwang595/pytorch_distributed_nn/blob/41be7dfc6719d2b4c9c1216035cd0126cf7dcecd/tools/pytorch_ec2.py#L934

This sets up a cluster with NFS. Take part of this?

Look at his tests to see how he runs.
