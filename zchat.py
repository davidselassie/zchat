import sys
import time

from client import ServerConnector
from server import ClientHandler


def handle_message(in_msg):
    print('>', in_msg)
    print('<', in_msg)
    return in_msg


def run_server():
    ch = ClientHandler()
    while True:
        if ch.client_count > 0:
            ch.recv_send(handle_message)
        else:
            time.sleep(0.5)


def run_client():
    sc = ServerConnector('localhost')
    while True:
        out_msg = input('? ')
        print('<', out_msg)
        in_msg = sc.send_recv(out_msg)
        print('>', in_msg)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'server':
        run_server()
    elif cmd == 'client':
        run_client()
    else:
        raise ValueError('unknown command')
