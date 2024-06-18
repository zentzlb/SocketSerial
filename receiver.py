import pickle
import socket
from _thread import start_new_thread, exit

import sys


# HOST = socket.gethostbyname(socket.gethostname())  # Standard loopback interface address (localhost)
# PORT = 5555  # Port to listen on (non-privileged ports are > 1023)


class Receiver:
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
                    print(f"connected to: {addr}")
                    start_new_thread(self.control, (conn,))
                except OSError as e:
                    print(e)

    def control(self, conn: socket.socket):

        print('starting')
        with conn:
            while self.run:
                try:
                    data = pickle.loads(conn.recv(2048))
                    self.data = data
                    print(data)
                except EOFError as e:
                    print(e)
                    conn.close()
                    return
                except ConnectionResetError as e:
                    print(e)
                    conn.close()
                    return


if __name__ == '__main__':
    r = Receiver(5555)
    r.main()
