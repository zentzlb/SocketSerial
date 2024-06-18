import pickle
import socket
from _thread import start_new_thread, exit
import time
from typing import Callable, Any

import sys


# HOST = socket.gethostbyname(socket.gethostname())  # Standard loopback interface address (localhost)
# PORT = 5555  # Port to listen on (non-privileged ports are > 1023)


class Receiver:

    host = socket.gethostbyname(socket.gethostname())

    def __init__(self, port: int):
        self.run = True
        self.port = port
        self.conn: None | socket.socket = None
        self.data: Any = None
        # atexit.register(self.close)

    def close(self):
        self.run = False
        raise SystemExit

    def main(self):
        print('main')
        print('here')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            conn.bind((self.host, self.port))
            conn.listen()
            print('connect')
            while self.run:
                try:
                    conn, addr = conn.accept()
                    print(f"\nConnected to: {addr}")
                    start_new_thread(self.listen, (conn, addr))
                except OSError as e:
                    print(e)

    # def connect(self):


    def listen(self, conn: socket.socket, addr: tuple):

        # print(f'Connection to {addr} Established -> Starting Thread')
        print('Starting Thread')
        run = True
        with conn:
            while run:
                try:
                    self.data = pickle.loads(conn.recv(1048576))
                    print(self.data)
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
