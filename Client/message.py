"""Client side message class
Authors:
   Peter Hamran        xhamra00@stud.fit.vutbr.cz
Date:
   02.05.2020
"""

import sys
import selectors
import json
import io
import struct


class Message:

    def __init__(self, selector, sock, addr, request):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.request = request
        self._recv_buffer = b""
        self._send_buffer = b""
        self._request_queued = False
        self._json_header_len = None
        self.json_header = None
        self.response = None

    def _set_selector_events_mask(self, mode):
        """ Set selector to listen for events: mode is 'r', 'w' or 'rw'. """
        if mode == 'r':
            events = selectors.EVENT_READ
        elif mode == 'w':
            events = selectors.EVENT_WRITE
        elif mode == 'rw':
            events = selectors.EVENT_WRITE | selectors.EVENT_READ
        else:
            raise ValueError(f'Invalid event mas mode {repr(mode)}.')
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            # Data ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError('Peer closed.')

    def _write(self):
        if self._send_buffer:
            ## TODO print send data??
            try:
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]

    @staticmethod
    def _json_encode(obj, encoding):
        return json.dump(obj, ensure_ascii=False).encode(encoding)

    @staticmethod
    def _json_decode(json_bytes, encoding):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=''
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _create_message(self, *, content_bytes, content_type, content_encoding):
        json_header = {
            'byteorder': sys.byteorder,
            'content-type': content_type,
            'content-encoding': content_encoding,
            'content-length': len(content_bytes),
        }

        json_header_bytes = self._json_encode(json_header, 'utf-8')

        message_header = struct.pack('>H', len(json_header_bytes))
        message = message_header + json_header_bytes + content_bytes

        return message

    def _process_response_json_content(self):
        content = self.response
        result = content.get('result')
        print(f'Got result: {result}')

    def _process_response_binary_content(self):
        content = self.response
        print(f'Got response: {repr(content)}')

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()

        if self._json_header_len is None:
            self.process_proto_header()

        if self._json_header_len is not None:
            if self.json_header is None:
                self.process_json_header()

        if self.json_header:
            if self.response is None:
                self.process_response()

    def write(self):
        if not self._request_queued:
            self.queue_request()

            self._write()

        if self._request_queued:
            if not self._send_buffer:
                self._set_selector_events_mask('r')

    def close(self):
        print('Closing conntection to ', self.addr)

        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(f'Error: selector.unregister() exception for', f'{self.addr}: {repr(e)}')

        try:
            self.sock.close()
        except OSError as e:
            print(f'error: socket.close() exception for', f'{self.addr}: {repr(e)}')
        finally:
            self.sock = None

    def queue_request(self):
        content = self.request['content']
        content_type = self.request['type']
        content_encoding = self.request['encoding']

        if content_type == 'text/json':
            req = {
                'content_bytes': self._json_encode(content, content_encoding),
                'content_type': content_type,
                'content_encoding': content_encoding,
            }
        else:
            req = {
                'content_bytes': content,
                'content_type': content_type,
                'content_encoding': content_encoding,
            }

        message = self._create_message(**req)
        self._send_buffer += message
        self._request_queued = True

    def process_proto_header(self):
        hdrlen = 2

        if len(self._recv_buffer) >= hdrlen:
            self._json_header_len = struct.unpack(
                '>H', self._recv_buffer[:hdrlen]
            )[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def process_json_header(self):
        hdrlen = self._json_header_len

        if len(self._recv_buffer) >= hdrlen:
            self.json_header = self._json_decode(
                self._recv_buffer[:hdrlen], 'utf-8'
            )
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in ('byteorder', 'content-length', 'content-type', 'content-encoding'):
                if reqhdr not in self.json_header:
                    raise ValueError(f'Missing required header "{reqhdr}".')

    def process_response(self):
        content_len = self.json_header['content-length']
        if not len(self._recv_buffer) >= content_len:
            return
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.json_header['content-type'] == 'text/json':
            encoding = self.json_header['content-encoding']
            self.response = self._json_decode(data, encoding)
            # TODO print received data
            self._process_response_json_content()
        else:
            self.response = data
            print(f'Received {self.json_header["content-type"]} response from', self.addr)
            self._process_response_binary_content()

        self.close()
