def upload_thought(address, user_id, thought):
    from ..utils import Thought
    from datetime import datetime
    message = Thought(user_id, datetime.now(), thought)
    from socket import socket
    sock = socket()
    sock.connect(address)
    from ..utils import Connection
    conn = Connection(sock)
    conn.send(message.serialize())
    print("done")


# def upload(address, user, thought):
#     if isinstance(address, str):
#         host, port = address.split(':')
#         address = (host, int(port))
#     upload_thought(address, user, thought)


# def main(argv):
#     if len(argv) != 4:
#         print(f'USAGE: {argv[0]} <address> <user> <thought>')
#         return 1
#     try:
#         ip, port = argv[1].split(':')
#         upload((ip, int(port)), argv[2], argv[3])
#         return 0
#     except Exception as error:
#         print(f'ERROR: {error}')
#         return 1


# if __name__ == '__main__':
#     from sys import argv, exit
#     exit(main(argv))
