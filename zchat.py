import sys

from server import block_collect_clients
from client import ServerConnector


def join_and_respond(msgs_in):
    msg_out = '&'.join(msgs_in)
    print('>', msg_out)
    return msg_out


def run_server():
    print('starting server')
    print('registation started')
    clients = block_collect_clients()
    print('registration over')
    print(clients.client_count, 'clients connected')

    while True:
        clients.recv_send(join_and_respond)


def run_client():
    print('starting client')
    connector = ServerConnector('localhost')
    print('registered')

    cmd = 'wait'
    while cmd == 'wait':
        print(connector.get_client_count(), 'clients connected')
        cmd = input('wait, join, or close? ')
        if cmd == '':
            cmd = 'wait'
        if cmd == 'close':
            connector.stop_register()
    server = connector.connect()

    while True:
        msg_in = input('> ')
        msg_out = server.send_recv(msg_in)
        print('<', msg_out)


if __name__ == '__main__':
    if sys.argv[1] == 'server':
        run_server()
    else:
        run_client()
