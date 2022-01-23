import cv2
import numpy as np
import sys
import os
from time import localtime, strftime

onRoadOffset = 0.1
onRoadThreshold_day = 120
onRoadThreshold_night = 85
snowfallThreshold = 10

def snowDetection(ref, test, log):
    """Detects in test video the snowfall rate and
    if there is snow on the road or not. Uses a reference video to
    test the video.

    Args:
        ref (str): path to reference video
        test (str): path to test video
        log (bool): indicates if a csv logfile and logvids must be made for this test

    Returns:
        (bool, float): tuple containing test results in the following format : [snowOnRoad, snowfallRates]
    """
    
    refCap = cv2.VideoCapture(ref)
    
    if not refCap.isOpened():
        print("Can't open reference video")
        exit()
        
    testCap = cv2.VideoCapture(test)
    
    if not testCap.isOpened():
        print("Can't open test video")
        exit()
        
    frame_width = int(refCap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(refCap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    totalPixels = frame_height*frame_width
    
    frame_size = (int(frame_width), int(frame_height))    
    
    fps = 20
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    out_ref = cv2.VideoWriter("log/ref.avi", fourcc, fps, frame_size)
    out_test = cv2.VideoWriter("log/test.avi", fourcc, fps, frame_size)
    
    out_refNoise = cv2.VideoWriter("log/refNoise.avi", fourcc, fps, frame_size)
    out_refBack = cv2.VideoWriter("log/refBack.avi", fourcc, fps, frame_size)
    out_refNoiseThres = cv2.VideoWriter("log/refNoiseThres.avi", fourcc, fps, frame_size)
    out_refBackThres = cv2.VideoWriter("log/refBackThres.avi", fourcc, fps, frame_size)
    
    out_testNoise = cv2.VideoWriter("log/testNoise.avi", fourcc, fps, frame_size)
    out_testBack = cv2.VideoWriter("log/testBack.avi", fourcc, fps, frame_size)
    out_testNoiseThres = cv2.VideoWriter("log/testNoiseThres.avi", fourcc, fps, frame_size)
    out_testBackThres = cv2.VideoWriter("log/testBackThres.avi", fourcc, fps, frame_size)
        
    
    refNoiseRatios = []
    refSnowRatios = []     
       
    testNoiseRatios = []
    testSnowRatios = []        
    
    # tests with 60 double frames
    for i in range(60):
        # get reference double frames
        check1, refFrame1 = refCap.read()
        check2, refFrame2 = refCap.read()
        
        # get test double frames
        check3, testFrame1 = testCap.read()
        check4, testFrame2 = testCap.read()
        
        if check1 and check2 and check3 and check4:
            # Create noise and background ref frames
            refNoise = cv2.subtract(refFrame1, refFrame2)
            refBackground = cv2.subtract(refFrame1, refNoise)
            
            # Create noise and background test frames
            testNoise = cv2.subtract(testFrame1, testFrame2)
            testBackground = cv2.subtract(testFrame1, testNoise)
            #testBackground = testFrame1
               
            # Create thresholds frame
            refNoiseGrey = cv2.cvtColor(refNoise, cv2.COLOR_BGR2GRAY)
            th, refNoiseThres = cv2.threshold(refNoiseGrey, snowfallThreshold, 255, cv2.THRESH_BINARY)
            refBackgroundGrey = cv2.cvtColor(refBackground, cv2.COLOR_BGR2GRAY)
            th, refBackThres = cv2.threshold(refBackgroundGrey, onRoadThreshold_night, 255, cv2.THRESH_BINARY)
            
            testNoiseGrey = cv2.cvtColor(testNoise, cv2.COLOR_BGR2GRAY)
            th, testNoiseThres = cv2.threshold(testNoiseGrey, snowfallThreshold, 255, cv2.THRESH_BINARY)
            testBackgroundGrey = cv2.cvtColor(testBackground, cv2.COLOR_BGR2GRAY)
            th, testBackThres = cv2.threshold(testBackgroundGrey, onRoadThreshold_night, 255, cv2.THRESH_BINARY)
            
            if log:
                out_ref.write(refFrame1)
                out_test.write(testFrame1)
            
                out_refNoise.write(refNoise)
                out_refBack.write(refBackground)
                refNoiseThres = cv2.cvtColor(refNoiseThres, cv2.COLOR_GRAY2BGR)
                out_refNoiseThres.write(refNoiseThres)
                refBackThres = cv2.cvtColor(refBackThres, cv2.COLOR_GRAY2BGR)
                out_refBackThres.write(refBackThres)
                
                out_testNoise.write(testNoise)
                out_testBack.write(testBackground)
                testNoiseThres = cv2.cvtColor(testNoiseThres, cv2.COLOR_GRAY2BGR)
                out_testNoiseThres.write(testNoiseThres)
                testBackThres = cv2.cvtColor(testBackThres, cv2.COLOR_GRAY2BGR)
                out_testBackThres.write(testBackThres)
                        
            refNoiseRatios.append(np.sum(refNoiseThres == 255)/totalPixels)
            refSnowRatios.append(np.sum(refBackThres == 255)/totalPixels)
            
            testNoiseRatios.append(np.sum(testNoiseThres == 255)/totalPixels)
            testSnowRatios.append(np.sum(testBackThres == 255)/totalPixels)            
            
        else:
            break
        
    refCap.release()
    testCap.release()
    
    if log:
        out_ref.release()
        out_test.release()
    
        out_refNoise.release()
        out_refBack.release()
        out_refNoiseThres.release()
        out_refBackThres.release()
        
        out_testNoise.release()
        out_testBack.release()
        out_testNoiseThres.release()
        out_testBackThres.release()
    
    refNoiseRatio = np.average(refNoiseRatios)
    refSnowRatio = np.average(refSnowRatios)
    
    testNoiseRatio = np.average(testNoiseRatios)
    testSnowRatio = np.average(testSnowRatios)
                
    snowfallRate = (testNoiseRatio - refNoiseRatio)*100
    snowyRoad = testSnowRatio >= refSnowRatio+onRoadOffset

    return (snowyRoad, testNoiseRatio*100)

def snowfallRate(video, day, realDegree, log):

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

            #cv2.imshow("Test", noise_thres)

            snow_pixels = np.sum(noise_thres==255)
            snowRatios.append(snow_pixels/total_pixels)

            #if cv2.waitKey(1) == ord('q'):
            #    print("Quitting...")
            #    break

        else:
            #print("Video finished")
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