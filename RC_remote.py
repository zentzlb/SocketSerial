from network import Network
from server import Server
import serial
import time
from receiver import Receiver


class Bridge:

    # arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.001)
    receiver = Receiver(5555)
    receiver.main()
    run = True
    data = (0, 0)

    def main(self):
        """
        main loop
        :return:
        """
        with serial.Serial(port='COM3', baudrate=115200, timeout=.001) as arduino:
            time.sleep(1)
            while self.run:
                if self.data != self.receiver.data:
                    self.data = self.receiver.data
                    self.serial_write(f"{self.data[0]};{self.data[1]}", arduino)

    def serial_write(self, x: str, arduino: serial.Serial):
        """
        write to serial port
        :param x: string to send
        :param arduino: serial object
        :return:
        """
        b = bytes(x + '\r\n', 'utf-8')
        arduino.write(b)
        print(b)




# def write_line(x):
#     b = bytes(x + '\r\n',   'utf-8')
#     print(b)
#     # print(b.decode('utf-8'))
#     arduino.write(b)
#     data = arduino.readline()
#     arduino.flush()
#     return data


if __name__ == '__main__':
    bridge = Bridge()
    bridge.main()
    # arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.001)
    # time.sleep(1)
    # while True:
    #     value = write_line(f"{bridge.receiver.data[0]};{bridge.receiver.data[1]}")
    #     time.sleep(0.2)
