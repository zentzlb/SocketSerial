import pickle
import socket
from _thread import start_new_thread, exit
import time

import sys


# HOST = socket.gethostbyname(socket.gethostname())  # Standard loopback interface address (localhost)
# PORT = 5555  # Port to listen on (non-privileged ports are > 1023)


class Remote:
    host = socket.gethostbyname(socket.gethostname())
    data = (0, 0)
    run = True
    print(host)

    def __init__(self, port: int):
        self.port = port
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
                    start_new_thread(self.control, (conn, addr))
                except OSError as e:
                    print(e)

    def control(self, conn: socket.socket, addr: tuple):

        # print(f'Connection to {addr} Established -> Starting Thread')
        print('Starting Thread')
        run = True
        with conn:
            while run:
                try:
                    pickled_data = pickle.dumps(self.data)
                    conn.sendall(pickled_data)
                    time.sleep(0.01)
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
    r = Remote(5555)
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
