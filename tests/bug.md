[ec2-user@ip-172-31-19-144 tests]$ mpirun -n 2 -hostfile hosts_file ls
------------------------------------------------------------
A process or daemon was unable to complete a TCP connection
to another process:
  Local host:    ip-172-31-18-30
  Remote host:   172.31.19.144
This is usually caused by a firewall on the remote host. Please
check that any firewall (e.g., iptables) has been disabled and
try again.
------------------------------------------------------------
--------------------------------------------------------------------------
ORTE was unable to reliably start one or more daemons.
This usually is caused by:

* not finding the required libraries and/or binaries on
  one or more nodes. Please check your PATH and LD_LIBRARY_PATH
  settings, or configure OMPI with --enable-orterun-prefix-by-default

* lack of authority to execute on one or more specified nodes.
  Please verify your allocation and authorities.

* the inability to write startup files into /tmp (--tmpdir/orte_tmpdir_base).
  Please check with your sys admin to determine the correct location to use.

*  compilation of the orted with dynamic libraries when static are required
  (e.g., on Cray). Please check your configure cmd line and consider using
  one of the contrib/platform definitions for your system type.

* an inability to create a connection back to mpirun due to a
  lack of common network interfaces and/or no route found between
  them. Please check network connectivity (including firewalls
  and network routing requirements).

