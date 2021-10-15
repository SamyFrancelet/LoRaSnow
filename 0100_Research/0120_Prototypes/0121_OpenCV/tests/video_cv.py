import cv2

vid_capture = cv2.VideoCapture("Cars.mp4")

if (not vid_capture.isOpened()):
	print("Error opening the video file")
else:
	fps = int(vid_capture.get(5))
	print("FPS : ", fps)

	frame_count = vid_capture.get(7)
	print("Frame count : ", frame_count)

while(vid_capture.isOpened()):
	ret, frame = vid_capture.read()
	if ret == True:
		cv2.imshow("Frame", frame)

		key = cv2.waitKey(20)

		if key == ord('q'):
			break
	else:
		break

vid_capture.release()
cv2.destroyAllWindows()