import cv2 as cv
import numpy as np

from threshold_out import threshold_out

cam = cv.VideoCapture(0)

if not cam.isOpened():
    print("Can't open camera")
    exit()

frame_width = int(cam.get(3))
frame_height = int(cam.get(4))
frame_size = (frame_width, frame_height)

test = threshold_out(127, cv.THRESH_BINARY, 10, frame_size)

while True:
    check, frame = cam.read()

    if check:
        frame_grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        test.write(frame_grey, True)

        if cv.waitKey(1) == ord('q'):
            break

    else:
        break