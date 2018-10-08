# Rhys Read
# camControl main.py

import time

import numpy as np
import cv2

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    upper_body_cascade = cv2.CascadeClassifier('upper_body.xml')
    face_cascade = cv2.CascadeClassifier('face.xml')
    eye_cascade = cv2.CascadeClassifier('eye.xml')

    print("Resolution: " + str(cap.get(3)) + " x " + str(cap.get(4)))

    while True:
        # Return capture frame by frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)

        # Run the gray image through Canny edge detection
        edges = cv2.Canny(gray, 50, 100)

        # bodies = upper_body_cascade.detectMultiScale(gray, 1.3, 5)
        # for (x, y, w, h) in bodies:
        #     frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 1)
            region = gray[y: y + h, x: x + w]

            eyes = eye_cascade.detectMultiScale(region, 1.3, 5)
            for (ex, ey, ew, hw) in eyes:
                region = cv2.rectangle(region, (ex, ey), (ex+ew, ey+hw), (0, 255, 0), 1)
            cv2.imshow("Region", region)

        # Display the resulting frame
        cv2.imshow("Frame", frame)
        # Display the edge frame
        cv2.imshow("Edge", edges)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()
