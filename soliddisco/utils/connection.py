class Connection:

    @classmethod
    def connect(cls, ip, port):
        address = (ip, port)
        from socket import socket
        sock = socket()
        sock.connect(address)
        return Connection(sock)

    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        from_ip = self.socket.getsockname()[0]
        from_port = self.socket.getsockname()[1]
        to_ip = self.socket.getpeername()[0]
        to_port = self.socket.getpeername()[1]
        return f"<Connection from {from_ip}:{from_port} to {to_ip}:{to_port}>"

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, size):
        data = b''
        while len(data) < size:
            tmp = self.socket.recv(size - len(data))
            if not tmp:
                break
            data += tmp
        else:
            return data
        raise OSError

    def close(self):
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.close()
