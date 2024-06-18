import cv2
from cam_receiver import Receiver

receiver = Receiver(5555)
receiver.main()


while True:

    if (frame := receiver.data) is not None:
        cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
