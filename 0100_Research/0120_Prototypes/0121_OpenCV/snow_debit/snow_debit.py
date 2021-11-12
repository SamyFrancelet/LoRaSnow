import cv2 as cv
import numpy as np
import sys
import os
from time import localtime, strftime

from threshold_out import threshold_out

def main(show_image = False, show_whiteness = False):
    logFolder = "logs/" + strftime("%Y-%m-%d_%H%M%S", localtime()) + "/"
    os.makedirs(logFolder)
    cam = cv.VideoCapture(1)
    #cam = cv.VideoCapture('Vincent.mp4')

    if not cam.isOpened():
        print("Can't open camera")
        exit()

    frame_width = int(cam.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv.CAP_PROP_FRAME_HEIGHT))
    frame_size = (frame_width, frame_height)

    fps = 20 #cam.get(cv.CAP_PROP_FPS)
    #cam.set(cv.CAP_PROP_AUTO_EXPOSURE, 0.0)
    #cam.set(cv.CAP_PROP_EXPOSURE, 0.1)

    fourcc = cv.VideoWriter_fourcc('M','J','P','G')
    out_origin = cv.VideoWriter(logFolder + "original.avi", fourcc, fps, frame_size)
    out_grey = cv.VideoWriter(logFolder + "grey.avi", fourcc, fps, frame_size, False)

    thresholds = []

    for x in range(100, 250, 20):
        thresholds.append(threshold_out(logFolder, x, cv.THRESH_BINARY, fps, frame_size))

    f = open(logFolder + 'measure.csv', 'a')
    f.write('\n')
    f.close()

    while True:
        check, frame = cam.read()

        if check:
            out_origin.write(frame)
            cv.imshow("original", frame)

            frame_grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            out_grey.write(frame_grey)

            if show_image:
                cv.imshow("grey", frame_grey)

            for thr in thresholds:
                thr.write(frame_grey, show_whiteness, show_image)

            f = open(logFolder + 'measure.csv', 'a')
            f.write('\n')
            f.close()

            if cv.waitKey(1) == ord('q'):
                break

        else:
            print("Camera feed gone, exitting...")
            break

if __name__ == "__main__":
    if(len(sys.argv) > 2):
        main(sys.argv[1], sys.argv[2])
    else:
        main()