import pickle
import socket
from _thread import start_new_thread, exit
from typing import Any
import time

import sys


# HOST = socket.gethostbyname(socket.gethostname())  # Standard loopback interface address (localhost)
# PORT = 5555  # Port to listen on (non-privileged ports are > 1023)


class Transmitter:

    def __init__(self, port: int, host: str):
        self.run = True
        self.port = port
        self.conn: None | socket.socket = None
        self.host = host

    def close(self):
        self.run = False
        raise SystemExit

    def main(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.conn:
            run = True
            while run:
                try:
                    self.conn.connect((self.host, self.port))
                    run = False
                    print(self.conn)
                except socket.error as e:
                    print(e)
                    time.sleep(1)
                    self.main()
                except EOFError as e:
                    print(e)
                    time.sleep(1)
                    print('player already connected')
                    self.main()
                except ConnectionResetError as e:
                    print(e)
                    time.sleep(1)
                    self.main()

    def send(self, data: Any):
        self.conn.send(pickle.dumps(data))


if __name__ == '__main__':

    r = Transmitter(5555, "DEEP-BLUE")
    r.main()
    while True:
        nums = input("Enter multiple numbers: ")
        try:
            r.send(tuple([int(i) for i in nums.split(' ')]))
        except SyntaxError as e:
            print(e.msg)
        except ValueError as e:
            print(e.__traceback__.tb_frame.f_trace)

