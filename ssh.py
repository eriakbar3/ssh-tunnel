import telnetlib
import sys
from contextlib import contextmanager
from argparse import ArgumentParser
from getpass import getpass
from paramiko import (
    SSHClient,
    MissingHostKeyPolicy,
)


@contextmanager
def make_tunnel(ssh_user, ssh_password, ssh_host, ssh_port, dst_ip, dst_port,command):
    client = SSHClient()
    client.set_missing_host_key_policy(MissingHostKeyPolicy())
    client.connect(hostname=ssh_host, username=ssh_user, password=ssh_password, port=ssh_port)
    transport = client.get_transport()
    tunnel = transport.open_channel('direct-tcpip', (dst_ip, dst_port), ('127.0.0.1', 0))
    yield tunnel
    tunnel.close()
    client.close()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('ssh_user', type=str)
    parser.add_argument('ssh_host', type=str)
    parser.add_argument('dst_ip', type=str)
    parser.add_argument('dst_port', type=int)
    parser.add_argument('--ssh_port', type=int, default=22)
    parser.add_argument('ssh_password', type=str)
    parser.add_argument('command', type=str)
    args = parser.parse_args()

    try:
        with make_tunnel( **vars(args)) as channel:
            tn = telnetlib.Telnet()

            tn.sock = channel
            user = 'surv2-apps'
            password = 'Surv2bahagia'
            cmd = args.command
            logout = 'logout'
            nomore = 'environment no more';
            tn.write(user.encode('ascii')+b"\n")
            tn.write(password.encode('ascii')+b"\n")
            tn.write(nomore.encode('ascii')+b"\n")
            tn.write(cmd.encode('ascii')+b"\n")
            tn.write(logout.encode('ascii')+b"\n")
            tn.interact()
            
    except KeyboardInterrupt:
        print('Got KeyboardInterrupt, shutting down graceful')
    except Exception as e:
        print('Error:', e)
        sys.exit(1)
