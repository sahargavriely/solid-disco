import threading


class ClientHandler(threading.Thread):

    lock = threading.Lock()

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir

    def run(self):  # start invokes run
        from ..utils import Thought
        data = self.connection.receive(20)
        from struct import unpack
        data += self.connection.receive(int(unpack('<I', data[16:])[0]))
        message = Thought.deserialize(data)
        ClientHandler.lock.acquire()
        from pathlib import Path
        user_dir = f"{self.data_dir}/{message.user_id}"
        Path(user_dir).mkdir(parents=True, exist_ok=True)
        time_dir = str(message.timestamp).replace(' ', '_').replace(':', '-')
        p = Path(f"{user_dir}/{time_dir}.txt")
        new_line = '\n'
        if not p.is_file():
            new_line = ''
        with p.open(mode="a+") as f:
            f.write(new_line + message.thought)
            f.close()
        ClientHandler.lock.release()
        self.connection.close()


def run_server(address, data_dir):
    from ..utils import Listener
    server = Listener(address[1], address[0])
    server.start()
    while True:
        client_conn = server.accept()
        client_handler = ClientHandler(client_conn, data_dir)
        client_handler.start()


# def run(address, data_dir):
#     if isinstance(address, str):
#         host, port = address.split(':')
#         address = (host, int(port))
#     run_server(address, data_dir)


# def main(argv):
#     if len(argv) != 3:
#         print(f'USAGE: {argv[0]} <address> <data dir>')
#         return 1
#     try:
#         ip, port = argv[1].split(':')
#         run((ip, int(port)), argv[2])
#         return 0
#     except Exception as error:
#         print(f'ERROR: {error}')
#         return 1


# if __name__ == '__main__':
#     from signal import signal, SIGINT
#     from sys import argv, exit

#     def handler(sig, frame):
#         print()
#         exit(0)

#     signal(SIGINT, handler)
#     exit(main(argv))
