import zmq


def _register_loop(reg_socket):
    client_count = 0
    msg = ''

    while msg != 'stop':
        msg = reg_socket.recv_string()
        if msg == 'reg':
            client_count += 1
            reg_socket.send_string('ack')
        elif msg == 'stop':
            reg_socket.send_string('done')
        elif msg == 'count':
            reg_socket.send_string(str(client_count))
        else:
            raise ValueError('unknown reg command')

    return client_count


def block_collect_clients():
    context = zmq.Context()
    reg_socket = context.socket(zmq.REP)
    reg_socket.bind('tcp://*:5555')

    client_count = _register_loop(reg_socket)
    reg_socket.close()

    out_socket = context.socket(zmq.PUB)
    out_socket.bind('tcp://*:5556')
    in_socket = context.socket(zmq.PULL)
    in_socket.bind('tcp://*:5557')
    return _ClientConnections(client_count, out_socket, in_socket)


class _ClientConnections:
    def __init__(self, client_count, out_socket, in_socket):
        self.client_count = client_count
        self._out_socket = out_socket
        self._in_socket = in_socket

    def recv_send(self, callback):
        self._send(callback(self._recv()))

    def _recv(self):
        return [self._in_socket.recv_string() for _ in range(self.client_count)]

    def _send(self, msg):
        self._out_socket.send_string(msg)
