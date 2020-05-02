"""Client side communicator for TCP socket establishmend and comm efforts
Authors:
   Peter Hamran        xhamra00@stud.fit.vutbr.cz
Date:
   02.05.2020
"""
import selectors
import socket as S
import types

# LocalHost
HOST = '127.0.0.1'
# Port
PORT = 42000


class Communicator:

    def __init__(self, host, port):
        # Create selector for multiple connectiosn
        self.selector = selectors.DefaultSelector()
        # Create listening socket
        self.socket = self.__setup_socket(host, port)
        # Register the socket with selector
        self.selector.register(self.socket, selectors.EVENT_READ, data=None)

    def __accept_wrapper(self, sock):
        # Socket is ready to read
        connection, address = sock.accept()
        print('Server has acceppted connection from ', address)
        # Allow non-blocking connection
        connection.setblocking(False)
        # Data of bytes
        data = types.SimpleNamespace(addr=address, int=b"", out=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.register(connection, events, data=data)

    @staticmethod
    def __setup_socket(host, port):
        # Create TCP socket for IPv4
        socket = S.socket(S.AF_INET, S.SOCK_STREAM)
        # Bind the socket to provided host and port
        socket.bind((host, port))
        # Change socket to listening socket
        socket.listen()
        # Set blocking to false
        socket.setblocking(False)

        return socket


if __name__ == '__main__':
    comm = Communicator(HOST, PORT)
