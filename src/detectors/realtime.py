import cv2
import pytesseract
import numpy as np
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Function to capture the screen
def capture_screen(bbox=(300, 300, 1500, 1000)):
    cap_scr = np.array(ImageGrab.grab(bbox))
    cap_scr = cv2.cvtColor(cap_scr, cv2.COLOR_RGB2BGR)
    return cap_scr

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read() 

    recognized_text = pytesseract.image_to_string(frame)

    # Perform bounding box detection using Tesseract's built-in capabilities
    d = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]) > 0:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
            # Draw the detected text on the frame
            frame_with_text = frame.copy()
            frame_with_text = cv2.putText(frame_with_text, recognized_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Frame with Detected Text", frame_with_text)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
            
                
