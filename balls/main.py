import cv2
import numpy as np
from pathlib import Path
import json
import random

save_path = Path(__file__).parent
config_path = save_path / "config.json"
cv2.namedWindow("Image", cv2. WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2. WINDOW_GUI_NORMAL)

position = [0, 0]
clicked = False
def on_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clicked at {x}, {y}")
        global position
        global clicked
        position = [x, y]
        clicked = True

cv2.setMouseCallback("Image", on_click)

cam = cv2.VideoCapture(0)
lower1 = None
upper1 = None
lower2 = None
upper2 = None
lower3 = None
upper3 = None
balls = None
ball1 = None
ball2 = None
ball3 = None
if config_path.exists():
    with config_path.open("r") as f:
        js = json.load(f)
        if "ball1" in js and "ball2" in js and "ball3" in js:
            lower1 = np.array(js["ball1"]["lower1"], dtype="u1")
            upper1 = np.array(js["ball1"]["upper1"], dtype="u1") 
            lower2 = np.array(js["ball2"]["lower2"], dtype="u1")
            upper2 = np.array(js["ball2"]["upper2"], dtype="u1") 
            lower3 = np.array(js["ball3"]["lower3"], dtype="u1")
            upper3 = np.array(js["ball3"]["upper3"], dtype="u1") 
            ball1 = [lower1, upper1]
            ball2 = [lower2, upper2]
            ball3 = [lower3, upper3]
            balls = [ball1, ball2, ball3]
positions = []
d = 6.36 #cm
while cam.isOpened():
    ret, frame = cam.read()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('1'):
        lower1 = lower
        upper1 = upper
    if key == ord('2'):
        lower2 = lower
        upper2 = upper
    if key == ord('3'):
        lower3 = lower
        upper3 = upper
    if clicked:
        clicked = False
        color = hsv[position[1], position[0]]
        lower = np.clip(color * 0.9, 0, 255).astype("u1")
        upper = np.clip(color * 1.1, 0, 255).astype("u1")
        upper[1] = 255
        upper[2] = 255
    if lower1 is not None:
        inr = cv2.inRange(hsv, lower1, upper1)
        mask = cv2.morphologyEx(inr, cv2.MORPH_CLOSE,
                               np.ones((5,5), dtype="u1"))
        cv2.imshow("Mask", mask)
        contours, _ = cv2.findContours(mask,
                                        cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contour = max(contours, key = cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > 10:
                x = int(x)
                y = int(y)
                radius = int(radius)
                cv2.circle(frame, (x, y), radius, (255, 0, 0), 4)
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
    if lower2 is not None:
        inr = cv2.inRange(hsv, lower2, upper2)
        mask = cv2.morphologyEx(inr, cv2.MORPH_CLOSE,
                               np.ones((5,5), dtype="u1"))
        cv2.imshow("Mask", mask)
        contours, _ = cv2.findContours(mask,
                                        cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contour = max(contours, key = cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > 10:
                x = int(x)
                y = int(y)
                radius = int(radius)
                cv2.circle(frame, (x, y), radius, (255, 0, 0), 4)
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
    if lower3 is not None:
        inr = cv2.inRange(hsv, lower3, upper3)
        mask = cv2.morphologyEx(inr, cv2.MORPH_CLOSE,
                               np.ones((5,5), dtype="u1"))
        cv2.imshow("Mask", mask)
        contours, _ = cv2.findContours(mask,
                                        cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contour = max(contours, key = cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > 10:
                x = int(x)
                y = int(y)
                radius = int(radius)
                cv2.circle(frame, (x, y), radius, (255, 0, 0), 4)
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
    cv2.imshow("Image", frame) 

cam.release()
cv2.destroyAllWindows()

with config_path.open("w") as f:
    json.dump(
        {"ball1":{"lower1":None if lower1 is None else lower1.tolist(),
         "upper1":None if upper1 is None else upper1.tolist()
         },
         "ball2":{"lower2":None if lower2 is None else lower2.tolist(),
         "upper2":None if upper2 is None else upper2.tolist()
         },
         "ball3":{"lower3":None if lower3 is None else lower3.tolist(),
         "upper3":None if upper3 is None else upper3.tolist()
         },},
        f
    )