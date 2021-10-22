import cv2 as cv
import numpy as np

def main():
    resize = False
    cam = cv.VideoCapture(0)
    if not cam.isOpened():
        print("Can't open camera")
        exit()

    check, frame = cam.read()
    snowyArray = []

    if not check:
        print("Can't receive frame. Exiting...")
        exit()

    if resize:
        frame = cv.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv.INTER_LINEAR)

    h,w,c = frame.shape
    pixel_tot = h*w
    #text = "Total pixels :" + str(pixel_tot)
    org = (20,20)

    while True:
        check, frame = cam.read()

        if not check:
            print("Can't receive frame. Exiting...")
            break

        if resize:
            frame = cv.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv.INTER_LINEAR)

        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        th, frame = cv.threshold(frame, 127, 255, cv.THRESH_BINARY)
        pixel_white = np.sum(frame == 255)
        snowyness = 100 * pixel_white/pixel_tot
        snowyArray.append(snowyness)
        text = "Snowyness :{:.2f}%".format(snowyness)

        frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
        cv.putText(frame, text, org, fontFace=cv.FONT_HERSHEY_COMPLEX, fontScale=0.5, color=(0,0,255))
        cv.imshow('cam', frame)

        if cv.waitKey(1) == ord('q'):
            break

    cam.release()
    A = np.array(snowyArray)
    print("{:.2f}%".format(np.mean(A)))
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
