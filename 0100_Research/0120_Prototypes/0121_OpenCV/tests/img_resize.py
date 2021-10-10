import cv2
import numpy as np

# read image
image = cv2.imread("image.jpg")

h,w,c = image.shape
print("Original size : ", h,"x",w)

down_width = 200
down_height = 150
down_points = (down_width, down_height)
resize_down = cv2.resize(image, down_points, interpolation = cv2.INTER_LINEAR)

# Set rows and columns
up_width = 600
up_height = 400
up_points = (up_width, up_height)
# resize the image
resized_up = cv2.resize(image, up_points, interpolation = cv2.INTER_LINEAR)

cv2.imshow("down", resize_down)
cv2.waitKey()
cv2.imshow("up", resized_up)
cv2.waitKey()
cv2.destroyAllWindows()