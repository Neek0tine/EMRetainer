import easyocr
import numpy as np
import cv2

cap =cv2.VideoCapture('http://10.16.121.196:4747/video')
reader = easyocr.Reader(["en", "id"], gpu=True)

while True:
    _, frame = cap.read()
    result = reader.readtext(frame)
    for detection in result:
        top_left = tuple(detection[0][0])
        bottom_right = tuple(detection[0][2])
        text = detection[1]
        print(text)
        color = (255, 0, 0)
        img = cv2.rectangle(frame, top_left, bottom_right, color)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()