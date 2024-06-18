import pickle
import socket
from _thread import start_new_thread, exit
import time
from typing import Any

import sys


# HOST = socket.gethostbyname(socket.gethostname())  # Standard loopback interface address (localhost)
# PORT = 5555  # Port to listen on (non-privileged ports are > 1023)


class Receiver:
    host = socket.gethostbyname(socket.gethostname())
    run = True
    print(host)

    def __init__(self, port: int):
        self.port = port
        self.data: Any = None
        # atexit.register(self.close)

    def close(self):
        self.run = False
        raise SystemExit

    def main(self):
        start_new_thread(self.connect, tuple())

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            while self.run:
                try:
                    conn, addr = s.accept()
                    print(f"\nConnected to: {addr}")
                    start_new_thread(self.listen, (conn, addr))
                except OSError as e:
                    print(e)

    def listen(self, conn: socket.socket, addr: tuple):

        # print(f'Connection to {addr} Established -> Starting Thread')
        print('Starting Thread')
        run = True
        with conn:
            while run:
                try:
                    # time.sleep(0.01)
                    data = conn.recv(1048576)

                    self.data = pickle.loads(data)
                    print(data.__sizeof__())
                except EOFError as e:
                    run = False
                    print(e.__cause__)
                    print(f'Connection to {addr} Lost -> Closing Thread')
                except ConnectionResetError as e:
                    run = False
                    # print(f'Connection Name: {conn.getsockname()}')
                    print(e.__cause__)
                    print(f'Connection to {addr} Lost -> Closing Thread')
                except ConnectionAbortedError as e:
                    run = False
                    # print(f'Connection Name: {conn.getsockname()}')
                    print(e.__cause__)
                    print(f'Connection to {addr} Aborted -> Closing Thread')


if __name__ == '__main__':
    r = Receiver(5555)
    r.main()

