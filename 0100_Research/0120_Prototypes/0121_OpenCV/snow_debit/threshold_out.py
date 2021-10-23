import cv2 as cv
import numpy as np

class threshold_out:
    name = "thr_test"
    thres = 127
    thres_type = cv.THRESH_BINARY
    output = cv.VideoWriter()

    def __init__(self, thres, thres_type, fps, frame_size):
        self.name = "thr_{}".format(thres)
        self.thres = thres
        self.thres_type = thres_type
        fourcc = cv.VideoWriter_fourcc('M','J','P','G')
        self.output = cv.VideoWriter(self.name+".avi", fourcc, fps, frame_size)

    def write(self, frame_grey, whiteness):
        th, frame_thr = cv.threshold(frame_grey, self.thres, 255, self.thres_type)

        if whiteness:
            h,w = frame_grey.shape
            pixel_total = h*w
            org = (20,20)

            pixel_white = np.sum(frame_thr == 255)
            white_ratio = 100*pixel_white/pixel_total

            text = "White_ratio = {:.2f}%".format(white_ratio)

            frame_thr = cv.cvtColor(frame_thr, cv.COLOR_GRAY2BGR)
            cv.putText(frame_thr, text, org, fontFace=cv.FONT_HERSHEY_COMPLEX, fontScale=0.5, color=(0,0,255))

        else:
            frame_thr = cv.cvtColor(frame_thr, cv.COLOR_GRAY2BGR)

        cv.imshow(self.name, frame_thr)
        self.output.write(frame_thr)

    def release(self):
        self.output.release()