import cv2 as cv
import numpy as np


def main() :
    cap = cv.VideoCapture("snow_test.mp4")

    if not cap.isOpened() :
        print("Can't open file")
        exit()

    while True:
        check1, frame1 = cap.read()
        check2, frame2 = cap.read()

        if check1 and check2:
            frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH)/2)
            frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)/2)
            frame_resize = (frame_width, frame_height)

            frame1 = cv.resize(frame1, frame_resize, interpolation=cv.INTER_LINEAR)
            frame2 = cv.resize(frame2, frame_resize, interpolation=cv.INTER_LINEAR)
            #frame1 = cv.GaussianBlur(frame1, (25,25), 0)
            #frame2 = cv.GaussianBlur(frame2, (25,25), 0)

            noise = cv.subtract(frame1, frame2)
            #noise = cv.absdiff(frame1, frame2)
            road = cv.subtract(frame1, noise)
            #road = cv.absdiff(frame1, noise)
            #road = cv.subtract(road, noise2)
            #road = cv.GaussianBlur(road, (25,25), 0)
            noise_grey = cv.cvtColor(road, cv.COLOR_BGR2GRAY)

            th, noise_thres = cv.threshold(noise_grey, 80, 255, cv.THRESH_BINARY)

            cv.imshow("Original", frame1)
            cv.imshow("Noise", noise)
            cv.imshow("Snow", noise_thres)
            cv.imshow("Road", road)

            if cv.waitKey(10) == ord('q'):
                print("Quitting...")
                break
        else:
            print("No more video feed, quitting...")
            break

if __name__ == "__main__":
    main()