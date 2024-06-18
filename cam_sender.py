import pickle
import socket
import time
from typing import Any
from _thread import start_new_thread


class Transmitter:

    def __init__(self, host: str, port: int):

        self.host = host  # The server's hostname or IP address
        self.port = port  # The port used by the server
        self.conn: None | socket.socket = None
        self.run = True

    def main(self):
        start_new_thread(self.connect, tuple())

    def connect(self):
        print('starting')
        self.run = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            while self.run:
                try:
                    conn.connect((self.host, self.port))
                    self.run = False
                    self.conn = conn
                    print(conn)
                except socket.error as e:
                    print(e)
                    time.sleep(1)
                except EOFError as e:
                    print(e)
                    time.sleep(1)
                    print('player already connected')
            while True:
                try:
                    time.sleep(1)
                    # data = pickle.loads(s.recv(1048576))
                    # self.data = data
                    # print(data)
                except EOFError as e:
                    print(e)
                    conn.close()
                    self.main()
                    # return
                except ConnectionResetError as e:
                    print(e)
                    conn.close()
                    self.main()
                    # return

    def send(self, data: Any):
        if self.run:
            print('no connection to send data')
        else:
            try:
                data = pickle.dumps(data)
                print(data.__sizeof__())
                self.conn.sendall(data)
            except ConnectionResetError as e:
                print(e.__cause__)
                print(f'Connection Lost -> Closing Thread')
            except ConnectionAbortedError as e:
                print(e.__cause__)
                print(f'Connection Aborted -> Closing Thread')


if __name__ == '__main__':
    r = Transmitter(socket.gethostbyname('Zentz-LT'), 5555)
    r.main()
    while True:
        nums = input("Enter multiple numbers: ")
        try:
            r.send(tuple([int(i) for i in nums.split(' ')]))
        except SyntaxError as e:
            print(e.msg)
        except ValueError as e:
            print(e.__traceback__.tb_frame.f_trace)
