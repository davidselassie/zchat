import zmq


class ServerConnector:

    def __init__(self, hostname):
        context = zmq.Context()
        self._socket = context.socket(zmq.REP)
        self._socket.connect('tcp://{}:5555'.format(hostname))

    def recv_send(self, callback):
        in_msg = self._socket.recv_string()
        out_msg = callback(in_msg)
        self._socket.send_string(out_msg)
