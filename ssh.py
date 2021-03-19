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
def make_tunnel(ssh_user, ssh_password, ssh_host, ssh_port, dst_ip, dst_port):
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
    args = parser.parse_args()
    password = getpass('Please enter the password: ')
    try:
        with make_tunnel(ssh_password=password, **vars(args)) as channel:
            tn = telnetlib.Telnet()
            
            tn.sock = channel
            tn.interact()
    except KeyboardInterrupt:
        print('Got KeyboardInterrupt, shutting down graceful')
    except Exception as e:
        print('Error:', e)
        sys.exit(1)
