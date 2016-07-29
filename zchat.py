import sys

import zmq


def run_server():
    ctx = zmq.Context()
    rs = ctx.socket(zmq.ROUTER)
    rs.get_monitor_socket()
    rs.bind('tcp://*:5555')
    while True:
        addr, _, msg = rs.recv_multipart()
        msg = msg.decode('utf-8')
        print('<', addr, msg)
        msg = 'back at ya ' + repr(addr)
        print('>', msg)
        msg = msg.encode('utf-8')
        rs.send_multipart((addr, b'', msg))


def run_client():
    ctx = zmq.Context()
    rs = ctx.socket(zmq.REQ)
    rs.connect('tcp://localhost:5555')
    while True:
        msg = 'hi'
        print('<', msg)
        rs.send_string(msg)
        msg = rs.recv_string()
        print('> ', msg)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'server':
        run_server()
    elif cmd == 'client':
        run_client()
    else:
        raise ValueError('unknown command')
