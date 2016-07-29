import zmq


class ServerConnector:

    def __init__(self, hostname):
        self._hostname = hostname

        self._context = zmq.Context()
        self._reg_socket = self._context.socket(zmq.REQ)
        self._reg_socket.connect('tcp://{}:5555'.format(self._hostname))
        if self._send_recv('reg') != 'ack':
            raise ConnectionError("server wasn't accepting registrations")

    def stop_register(self):
        if self._send_recv('stop') != 'done':
            raise ConnectionError("server wasn't accepting registrations")
        self._reg_socket = None

    def get_client_count(self):
        return int(self._send_recv('count'))

    def _send_recv(self, msg):
        self._reg_socket.send_string(msg)
        return self._reg_socket.recv_string()

    def connect(self):
        in_socket = self._context.socket(zmq.SUB)
        in_socket.connect('tcp://{}:5556'.format(self._hostname))
        # Must subscribe to something to get all messages.
        in_socket.setsockopt_string(zmq.SUBSCRIBE, '')
        out_socket = self._context.socket(zmq.PUSH)
        out_socket.connect('tcp://{}:5557'.format(self._hostname))
        self._reg_socket = None
        return _ServerConnection(in_socket, out_socket)


class _ServerConnection:
    def __init__(self, in_socket, out_socket):
        self._in_socket = in_socket
        self._out_socket = out_socket

    def send_recv(self, msg):
        self._out_socket.send_string(msg)
        return self._in_socket.recv_string()
