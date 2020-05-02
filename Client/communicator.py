"""Client side communicator for TCP socket establishmend and comm efforts
Authors:
   Peter Hamran        xhamra00@stud.fit.vutbr.cz
Date:
   02.05.2020
"""
import sys
import socket
import selectors
import traceback

# LocalHost
HOST = '127.0.0.1'
# Port
PORT = 42000


class Communicator:

    def __init__(self, host, port):
        self.selector = selectors.DefaultSelector()
        self.sock = self._create_socket()

    def create_request(self, action, piece):
        pass

    @staticmethod
    def _create_socket():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock

    def start_connection(self, host, port, request):
        addr = (host, port)
        print('Starting connection to ', addr)


if __name__ == '__main__':
    pass
