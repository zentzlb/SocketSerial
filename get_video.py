import cv2
from cam_sender import Transmitter
import socket

vid = cv2.VideoCapture(0)
transmitter = Transmitter(socket.gethostbyname('zentz-lt'), 5555)
transmitter.main()

while True:
    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    transmitter.send(frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break