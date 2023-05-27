# Details
# image size:       480 X 640
# turn right:       negative setW
from GUI import GUI
from HAL import HAL
import cv2
import numpy as np

# Enter sequential code!
img = HAL.getImage()

cx = 320
speed = 2
freq = 12
Ts = 1/freq

ePrev = 0
eAccum = 0




    
while True:
    # Enter iterative code!
    img = HAL.getImage()
    HAL.setV(speed)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100, 100])  # Red hue ranges from 0 to 10 and 170 to 180
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv_img, lower_red, upper_red)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (assuming it represents the red area)
    largest_contour = max(contours, key=cv2.contourArea)

    # Calculate the centroid of the largest contour
    M = cv2.moments(largest_contour)
    centroid_x = int(M['m10'] / M['m00'])
    centroid_y = int(M['m01'] / M['m00'])
    
    eCurr = (cx - centroid_x)
    de = (eCurr - ePrev)/Ts
    eAccum += Ts * (eCurr+ePrev)/2
  
    kp = 1/200
    ki = 1e-5
    kd = 1/500
    
    HAL.setW(kp*eCurr + ki*eAccum + kd*de)
    ePrev = eCurr
    GUI.showImage(img)