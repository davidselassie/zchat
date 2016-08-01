from threading import Thread

import zmq
from zmq.utils.monitor import recv_monitor_message


class _ConnectionCountUpdater(Thread):

    def __init__(self, socket, client_handler):
        super().__init__(daemon=True)

        self._monitor_socket = socket.get_monitor_socket()
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
        self._socket = context.socket(zmq.DEALER)
        self._count_updater = _ConnectionCountUpdater(self._socket, self)
        self._socket.bind('tcp://*:5555')

    def send_recv(self, msg):
        client_count = self.client_count
        for _ in range(client_count):
            self._socket.send_multipart((b'', msg.encode('utf-8')))
        for _ in range(client_count):
            empty_frame, msg_bytes = self._socket.recv_multipart()
            if empty_frame == b'':
                yield msg_bytes.decode('utf-8')
