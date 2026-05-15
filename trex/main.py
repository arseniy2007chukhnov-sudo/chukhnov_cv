import cv2 
from mss import MSS
import pyautogui as ptg
import time
import numpy as np
                                                                                                    
ptg.FAILSAFE = False
ptg.PAUSE = 0                            

cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)

monitor = {"top": 270, "left": 570, "width": 755, "height": 210}    
start_time = time.time()   
game_start_time = start_time


x1_a = 105                                                     
x2_a = 141
y1_a = 160
y2_a = 175
max_exp = 125


x1_b = 105
x2_b = 160            
y1_b = 100
y2_b = 140                                                                                       


with MSS() as mon:
    while True:
        sct = mon.grab(monitor)
        img = np.asarray(sct)
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

        cur_time = time.time()
        delta = cur_time - game_start_time
        speed_factor = 1.0 + (delta / 200.0)
        dc_x2_a = x2_a + int((speed_factor - 1.0) * max_exp)
        dc_x2_a = min(dc_x2_a, monitor['width'] - 10)
        dc_x2_b = x2_b + int((speed_factor - 1.0) * max_exp)
        dc_x2_b = min(dc_x2_b, monitor['width'] - 10)

        roi1 = mask[y1_a:y2_a, x1_a:dc_x2_a]
        S1 = np.sum(roi1) / 255.0

        roi2 = mask[y1_b:y2_b, x1_b:dc_x2_b]
        S2 = np.sum(roi2) / 255.0
        if S2 >100 and S1 < 10:
            ptg.keyDown("down")
            time.sleep(0.3  )
            ptg.keyUp("down")
            continue
        elif S1 >100 and S2 <85:
            ptg.press("space")
            time.sleep(0.13)
            ptg.keyDown("down")
            time.sleep(0.01)
            ptg.keyUp("down")
            continue
        elif S1 > 300:
            ptg.keyDown("space")            
            time.sleep(0.5)
            ptg.keyUp("down")
            continue
        elif S1 > 100:
            ptg.press("space")     
            continue
        cv2.rectangle(mask, (x1_a, y1_a), (dc_x2_a,y2_a), 255, 2)
        cv2.rectangle(mask, (x1_b, y1_b), (dc_x2_b, y2_b), 255, 2)
        cv2.imshow("Mask", mask) 

        time.sleep(0.005)

cv2.destroyAllWindows()