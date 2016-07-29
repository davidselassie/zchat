import zmq


class ServerConnector:

    def __init__(self, hostname):
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        self._socket.connect('tcp://{}:5555'.format(hostname))

    def send_recv(self, msg):
        self._socket.send_string(msg)
        return self._socket.recv_string()
