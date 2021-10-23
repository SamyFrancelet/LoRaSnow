import cv2 as cv
import numpy as np

from threshold_out import threshold_out

def main():
    cam = cv.VideoCapture(0)

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
    out_origin = cv.VideoWriter("original.avi", fourcc, fps, frame_size)
    out_grey = cv.VideoWriter("grey.avi", fourcc, fps, frame_size, False)

    thresholds = []

    for x in range(100, 250, 20):
        thresholds.append(threshold_out(x, cv.THRESH_BINARY, fps, frame_size))

    while True:
        check, frame = cam.read()

        if check:
            out_origin.write(frame)
            cv.imshow("original", frame)

            frame_grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            out_grey.write(frame_grey)
            cv.imshow("grey", frame_grey)

            for thr in thresholds:
                thr.write(frame_grey, True)

            if cv.waitKey(1) == ord('q'):
                break

        else:
            print("Camera feed gone, exitting...")
            break

if __name__ == "__main__":
    main()