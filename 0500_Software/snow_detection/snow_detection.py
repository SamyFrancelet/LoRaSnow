import cv2
import numpy as np
import sys
import os
from time import localtime, strftime

onRoadOffset = 0.1
onRoadThreshold_day = 120
onRoadThreshold_night = 85
snowfallThreshold = 10

def snowfallRate(video, day, realDegree, log):
    """Estimates snowfall rate on the video

    Args:
        video (str): path to video to test
        day (int): indicates if the video is during the day (1 = day, 0 = night)
        realDegree (int): indicates the degree of snowfall from 0 to 3
        log (str): path to log folder

    Returns:
        (float, int): tuple containing results in the following format : [snowfall rate, estimatedDegree]
    """

    cap = cv2.VideoCapture(video)

    if not cap.isOpened():
        print("Can't open file : " + video)
        exit()

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_resize = (frame_width, frame_height)
    total_pixels = frame_width*frame_height

    f = open(log + "snowfall.csv", 'a')
    f.write(str(day) + ',' + str(realDegree) + ',')
    f.close()

    snowRatios = []

    for i in range(120):
        check1, frame1 = cap.read()
        check2, frame2 = cap.read()

        if check1 and check2:
            noise = cv2.subtract(frame1, frame2)
            noise_grey = cv2.cvtColor(noise, cv2.COLOR_BGR2GRAY)
            th, noise_thres = cv2.threshold(noise_grey, snowfallThreshold, 255, cv2.THRESH_BINARY)


            snow_pixels = np.sum(noise_thres==255)
            snowRatios.append(snow_pixels/total_pixels)

        else:
            break

    rate = np.average(snowRatios)
    estimatedDegree = 0

    if rate < 1/100:
        estimatedDegree = 0
    elif rate < 2.5/100:
        estimatedDegree = 1
    elif rate < 7/100:
        estimatedDegree = 2
    else :
        estimatedDegree = 3

    f = open(log + "snowfall.csv", 'a')
    f.write(str(rate) + ',' + str(estimatedDegree) + '\n')
    f.close()

    return rate, estimatedDegree

def snowOnRoad(video, ref, day, realState, log, denoise=True):
    """Estimates snow coverage on the road from video

    Args:
        video (str): path to video to test
        ref (float): white ratio from reference video
        day (int): indicates if the video is during the day (1 = day, 0 = night)
        realState (int): indicates the degree of snow on the road from 0 to 2
        log (str): path to log folder
        denoise (bool): indicates if the algorithm must use denoising or not

    Returns:
        (float, int): tuple containing results in the following format : [snowyness rate, estimatedSnowyness]
    """
    cap = cv2.VideoCapture(video)

    if not cap.isOpened():
        print("Can't open file : " + video)
        exit()

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_resize = (frame_width, frame_height)
    total_pixels = frame_width*frame_height

    f = open(log + "snowOnRoad.csv", 'a')
    f.write(str(day) + ',' + str(realState) + ',')
    f.close()

    snowRatios = []
    for i in range(60):
        check1, frame1 = cap.read()
        check2, frame2 = cap.read()

        if check1 and check2:
            if denoise:
                noise = cv2.subtract(frame1, frame2)
                back = cv2.subtract(frame1, noise)
                back_grey = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
            else:
                back_grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            
            if day == 1:
                th, back_thres = cv2.threshold(back_grey, onRoadThreshold_day, 255, cv2.THRESH_BINARY)
            else:
                th, back_thres = cv2.threshold(back_grey, onRoadThreshold_night, 255, cv2.THRESH_BINARY)

            #cv2.imshow("Test", back_thres)

            snow_pixels = np.sum(back_thres==255)
            snowRatios.append(snow_pixels/total_pixels)

            #if cv2.waitKey(1) == ord('q'):
            #    print("Quitting...")
            #    break

        else:
            #print("Video finished")
            break

    rate = np.average(snowRatios)
    snowyRoad = rate - ref
    estimatedSnowyness = 0

    if snowyRoad < 16/100:
        estimatedSnowyness = 0
    elif snowyRoad < 30/100:
        estimatedSnowyness = 1
    else :
        estimatedSnowyness = 2

    f = open(log + "snowOnRoad.csv", 'a')
    f.write(str(snowyRoad) + ',' + str(estimatedSnowyness) + '\n')
    f.close()

    return snowyRoad, estimatedSnowyness

def quickRatio(video, day, denoise=True):
    """Gives a quick white ratio, typically for a reference video

    Args:
        video (str): path to video to test
        day (int): indicates if the video is during the day (1 = day, 0 = night)
        denoise (bool): indicates if the algorithm must use denoising or not

    Returns:
        (float): white ratio in the video
    """


    cap = cv2.VideoCapture(video)

    if not cap.isOpened():
        print("Can't open file : " + video)
        exit()

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_resize = (frame_width, frame_height)
    total_pixels = frame_width*frame_height

    snowRatios = []
    for i in range(60):
        check1, frame1 = cap.read()
        check2, frame2 = cap.read()

        if check1 and check2:
            if denoise:
                noise = cv2.subtract(frame1, frame2)
                back = cv2.subtract(frame1, noise)
                back_grey = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
            else:
                back_grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            
            if day == 1:
                th, back_thres = cv2.threshold(back_grey, onRoadThreshold_day, 255, cv2.THRESH_BINARY)
            else:
                th, back_thres = cv2.threshold(back_grey, onRoadThreshold_night, 255, cv2.THRESH_BINARY)

            snow_pixels = np.sum(back_thres==255)
            snowRatios.append(snow_pixels/total_pixels)

        else:
            #print("Video finished")
            break

    return np.average(snowRatios)

def main():
    logFolder = "logs/" + strftime("%Y-%m-%d_%H%M%S", localtime()) + "/"
    os.makedirs(logFolder)

    f = open(logFolder + "snowOnRoad.csv", 'a')
    f.write("Day,Observed snow on road, White ratio on road, Estimated snow on road\n")
    f.close()

    dayRef = quickRatio("sorted/snowOnRoad/day/ref.mp4", 1, denoise=False)
    print(dayRef*100)
    nightRef = quickRatio("sorted/snowOnRoad/night/ref.mp4", 0, denoise=False)
    print(nightRef*100)

    for root, dirs, files in os.walk("sorted\snowOnRoad"):
        params = root.split('\\')
        day = 1
        ref = dayRef
        snowyness = 0
        if len(params) == 4:
            if params[2] == "day":
                day = 1
                ref = dayRef
            else:
                day = 0
                ref = nightRef

            if params[3] == "desnowd":
                snowyness = 0
            elif params[3] == "partiallySnowy":
                snowyness = 1
            elif params[3] == "snowy":
                snowyness = 2

            for file in files:
                print((day, snowyness))
                print(snowOnRoad(root + '\\' + file, ref, day, snowyness, logFolder, denoise=False))

    f = open(logFolder + "snowfall.csv", 'a')
    f.write("Day,Observed intensity, White ratio, Estimated intensity\n")
    f.close()

    for root, dirs, files in os.walk("sorted\snowfall"):
        params = root.split('\\')
        day = 1
        snowfall = 0
        if len(params) == 4:
            if params[2] == "day":
                day = 1
            else:
                day = 0

            if params[3] == "nothing":
                snowfall = 0
            elif params[3] == "smallSnow":
                snowfall = 1
            elif params[3] == "snowy":
                snowfall = 2
            elif params[3] == "lotSnowy":
                snowfall = 3

            for file in files:
                print((day, snowfall))
                #print(snowfallRate(root + '\\' + file, day, snowfall, logFolder))


if __name__ == "__main__":
    main()