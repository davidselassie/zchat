from threading import Thread

import zmq
from zmq.utils.monitor import recv_monitor_message


class _ConnectionCountUpdater(Thread):

    def __init__(self, client_handler):
        super().__init__(daemon=True)

        self._monitor_socket = client_handler._socket.get_monitor_socket()
        self._client_hadler = client_handler

        self.start()

    def run(self):
        while True:
            event_type = recv_monitor_message(self._monitor_socket)['event']
            if event_type == zmq.EVENT_ACCEPTED:
                self._client_hadler.client_count += 1
            elif event_type == zmq.EVENT_CLOSED or event_type == zmq.EVENT_DISCONNECTED:
                self._client_hadler.client_count -= 1


class ClientHandler:

    def __init__(self):
        self.client_count = 0

        context = zmq.Context()
        self._socket = context.socket(zmq.ROUTER)
        self._monitor = _ConnectionCountUpdater(self)
        self._socket.bind('tcp://*:5555')

    def recv_send(self, callback):
        for _ in range(self.client_count):
            addr, in_msg = self._recv()
            out_msg = callback(in_msg)
            self._send(addr, out_msg)

    def _recv(self):
        addr, _, msg_bytes = self._socket.recv_multipart()
        msg = msg_bytes.decode('utf-8')
        return addr, msg

    def _send(self, addr, msg):
        self._socket.send_multipart((addr, b'', msg.encode('utf-8')))
