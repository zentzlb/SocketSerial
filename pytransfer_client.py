import pickle
import socket
from _thread import start_new_thread, exit
import time

import sys


# HOST = socket.gethostbyname(socket.gethostname())  # Standard loopback interface address (localhost)
# PORT = 5555  # Port to listen on (non-privileged ports are > 1023)


class Tclient:

    def __init__(self, port: int, host: str):
        self.run = True
        self.port = port
        self.conn: None | socket.socket = None
        self.host = host
        # atexit.register(self.close)

    def close(self):
        self.run = False
        raise SystemExit

    def main(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            while self.run:
                try:
                    self.conn, addr = s.accept()
                    print(f"\nConnected to: {addr}")
                    self.receive(self.conn, addr)
                except OSError as e:
                    print(e)

    def send(self, name: str, file: str):
        data = pickle.dumps((name, file))
        self.conn.send(data)

    def receive(self, conn: socket.socket, addr: tuple):
        # print(f'Connection to {addr} Established -> Starting Thread')
        print(f'Receiving from {addr}')
        run = True
        with conn:
            while run:
                try:
                    name, data = pickle.loads(conn.recv(1048576))
                    with open(name, 'w+') as file:
                        file.write(data)
                except EOFError as e:
                    print(e)
                    # conn.close()
                    # return
                except ConnectionResetError as e:
                    print(e)
                    # conn.close()
                    # return


if __name__ == '__main__':
    r = Tclient(5555)
    r.main()
    while True:
        nums = input("Enter multiple numbers: ")
        try:
            r.data = tuple([int(i) for i in nums.split(' ')])
            print(r.data)
        except SyntaxError as e:
            print(e.msg)
        except ValueError as e:
            print(e.__traceback__.tb_frame.f_trace)
