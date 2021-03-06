class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        from socket import socket
        self.server = socket()

    def __repr__(self):
        return f"Listener(port={self.port}, host={self.host!r}, " \
                f"backlog={self.backlog}, reuseaddr={self.reuseaddr})"

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen(self.backlog)

    def stop(self):
        self.server.close()

    def accept(self):
        from .connection import Connection
        return Connection(self.server.accept()[0])

    def __enter__(self):
        self.start()

    def __exit__(self, exception, error, traceback):
        self.stop()
