# import the cv2 library
import cv2


# read image
#img_color = cv2.imread('test.jpg',cv2.IMREAD_COLOR)
img_grayscale = cv2.imread('test.jpg',cv2.IMREAD_GRAYSCALE)
#img_unchanged = cv2.imread('test.jpg',cv2.IMREAD_UNCHANGED)

#Displays image inside a window
#cv2.imshow('color image',img_color)  
cv2.imshow('grayscale image',img_grayscale)
#cv2.imshow('unchanged image',img_unchanged)

# Waits for a keystroke
cv2.waitKey(0)  

# Destroys all the windows created
cv2.destroyAllWindows() 


cv2.imwrite('grayscale.jpg',img_grayscale)