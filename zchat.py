import sys
import time

from client import ServerConnector
from server import ClientHandler


def handle_message(in_msg):
    print('>', in_msg)
    out_msg = input('? ')
    print('<', out_msg)
    return out_msg


def run_server():
    ch = ClientHandler()
    found = ['init']
    while True:
        if ch.client_count > 0:
            out_msg = '&'.join(found)
            print('<', out_msg)
            found = []
            for in_msg in ch.send_recv(out_msg):
                print('>', in_msg)
                found.append(in_msg)
        else:
            time.sleep(0.5)


def run_client():
    sc = ServerConnector('localhost')
    while True:
        sc.recv_send(handle_message)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'server':
        run_server()
    elif cmd == 'client':
        run_client()
    else:
        raise ValueError('unknown command')
