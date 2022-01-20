import cv2 as cv
import numpy as np
import sys
import os
from time import localtime, strftime

from threshold_out import threshold_out

def main(show_image = False, show_whiteness = True):
    logFolder = "logs/" + strftime("%Y-%m-%d_%H%M%S", localtime()) + "/"
    os.makedirs(logFolder)
    os.makedirs(logFolder + "thres/")
    os.makedirs(logFolder + "noise/")
    #cam = cv.VideoCapture(1)
    cam = cv.VideoCapture('snow_test.mp4')

    frame_width = int(cam.get(cv.CAP_PROP_FRAME_WIDTH)/2)
    frame_height = int(cam.get(cv.CAP_PROP_FRAME_HEIGHT)/2)
    frame_size = (frame_width, frame_height)

    fps = 20

    fourcc = cv.VideoWriter_fourcc('M','J','P','G')
    out_origin = cv.VideoWriter(logFolder + "original.avi", fourcc, fps, frame_size)
    out_grey = cv.VideoWriter(logFolder + "grey.avi", fourcc, fps, frame_size, False)
    out_noise = cv.VideoWriter(logFolder + "noise.avi", fourcc, fps, frame_size, False)

    thresholds_simple = []
    thresholds_noise = []

    for x in range(10, 210, 20):
        thresholds_simple.append(threshold_out(logFolder + "thres/", x, cv.THRESH_BINARY, fps, frame_size))
        thresholds_noise.append(threshold_out(logFolder + "noise/", x, cv.THRESH_BINARY, fps, frame_size))

    f = open(logFolder + 'thres/measure.csv', 'a')
    f.write('\n')
    f.close()

    f = open(logFolder + 'noise/measure.csv', 'a')
    f.write('\n')
    f.close()

    if not cam.isOpened():
        print("Can't open camera")
        exit()

    while True:
        check1, frame1 = cam.read()
        check2, frame2 = cam.read()

        if check1 and check2:
            frame1 = cv.resize(frame1, frame_size, interpolation=cv.INTER_LINEAR)
            frame2 = cv.resize(frame2, frame_size, interpolation=cv.INTER_LINEAR)

            out_origin.write(frame1)
            cv.imshow("original", frame1)

            frame_grey = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
            out_grey.write(frame_grey)

            frame_noise = cv.cvtColor(cv.subtract(frame1, frame2), cv.COLOR_BGR2GRAY)
            out_noise.write(frame_noise)

            if show_image:
                cv.imshow("grey", frame_grey)
                cv.imshow("noise", frame_noise)

            for thr in thresholds_simple:
                thr.write(frame_grey, show_whiteness, show_image)

            for thr in thresholds_noise:
                thr.write(frame_noise, show_whiteness, show_image)

            f = open(logFolder + 'thres/measure.csv', 'a')
            f.write('\n')
            f.close()

            f = open(logFolder + 'noise/measure.csv', 'a')
            f.write('\n')
            f.close()

            if cv.waitKey(1) == ord('q'):
                break

        else:
            print("No more video feed, quitting...")
            break

    out_origin.release()
    out_grey.release()
    out_noise.release()

    for thr in thresholds_simple:
        thr.release()

    for thr in thresholds_noise:
        thr.release()

if __name__ == "__main__":
    if(len(sys.argv) > 2):
        main(sys.argv[1], sys.argv[2])
    else:
        main()