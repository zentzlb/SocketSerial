import pickle
import socket
import time
from _thread import start_new_thread


class Remote:
    data = (0, 0)

    def __init__(self, host: str, port: int):

        self.host = host  # The server's hostname or IP address
        self.port = port  # The port used by the server

    def control(self):
        print('starting')
        run = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.port))
                print(s)
            except socket.error as e:
                print(e)
            except EOFError as e:
                print(e)
                print('player already connected')
            while run:
                pickled_data = pickle.dumps(self.data)
                s.sendall(pickled_data)
                time.sleep(0.01)
                # data = s.recv(1024)

    def start_thread(self):
        start_new_thread(self.control, tuple())


if __name__ == '__main__':
    r = Remote('192.168.1.70', 5555)
    r.start_thread()
    while True:
        nums = input("Enter multiple numbers: ")
        r.data = tuple([int(i) for i in nums.split(' ')])
        print(r.data)
