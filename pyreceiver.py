import pickle
import socket
import time
from _thread import start_new_thread


class Receiver:
    data = (0, 0)

    def __init__(self, host: str, port: int):

        self.host = host  # The server's hostname or IP address
        self.port = port  # The port used by the server

    def control(self):
        print('starting')
        run = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            while run:
                try:
                    s.connect((self.host, self.port))
                    run = False
                    print(s)
                except socket.error as e:
                    print(e)
                    time.sleep(1)
                except EOFError as e:
                    print(e)
                    time.sleep(1)
                    print('player already connected')
            while True:
                try:
                    data = pickle.loads(s.recv(2048))
                    self.data = data
                    print(data)
                except EOFError as e:
                    print(e)
                    s.close()
                    self.control()
                    # return
                except ConnectionResetError as e:
                    print(e)
                    s.close()
                    self.control()
                    # return

    def start_thread(self):
        start_new_thread(self.control, tuple())


if __name__ == '__main__':
    r = Receiver(socket.gethostbyname('Zentz-LT'), 5555)
    r.control()
