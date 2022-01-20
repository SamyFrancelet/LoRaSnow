import cv2
import numpy as np

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
    
    onRoadOffset = 0.1
    onRoadThreshold = 80
    snowfallThreshold = 20
    
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
                
            # Create thresholds frame
            refNoiseGrey = cv2.cvtColor(refNoise, cv2.COLOR_BGR2GRAY)
            th, refNoiseThres = cv2.threshold(refNoiseGrey, snowfallThreshold, 255, cv2.THRESH_BINARY)
            refBackgroundGrey = cv2.cvtColor(refBackground, cv2.COLOR_BGR2GRAY)
            th, refBackThres = cv2.threshold(refBackgroundGrey, onRoadThreshold, 255, cv2.THRESH_BINARY)
            
            testNoiseGrey = cv2.cvtColor(testNoise, cv2.COLOR_BGR2GRAY)
            th, testNoiseThres = cv2.threshold(testNoiseGrey, snowfallThreshold, 255, cv2.THRESH_BINARY)
            testBackgroundGrey = cv2.cvtColor(testBackground, cv2.COLOR_BGR2GRAY)
            th, testBackThres = cv2.threshold(testBackgroundGrey, onRoadThreshold, 255, cv2.THRESH_BINARY)
            
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

def main():
    ref = "100-172719-172810.mp4"
    test = "420-021927-022427.mp4"

    results = snowDetection(ref, test, True)
    
    print(results)

if __name__ == "__main__":
    main()