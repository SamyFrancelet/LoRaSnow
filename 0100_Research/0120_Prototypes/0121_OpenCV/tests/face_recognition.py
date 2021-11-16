import cv2

def detect_faces(f_cascade, img, scaleFactor = 1.1):
    # copy the image to grayscale it
    face_img = img.copy()

    # Convert to grayscale
    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)

    # Detects multiscale (which image is closer to camera)
    faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5)

    # Go over every faces and draws green rectangles on top of img
    for (x, y, w, h) in faces :
        cv2.rectangle(face_img, (x,y), (x+w, y+h), (0, 255, 0), 2)

    return face_img

if __name__ == '__main__':
    haar_face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_alt.xml')
    cam = cv2.VideoCapture(0)

    while True:
        check, frame = cam.read()
        face_frame = detect_faces(haar_face_cascade, frame)

        cv2.imshow('cam', face_frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
