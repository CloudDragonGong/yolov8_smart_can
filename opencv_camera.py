import time

import cv2
import os
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 200)
cap.set(cv2.CAP_PROP_EXPOSURE, -2)
for i in range(2):
    _,img  = cap.read()
cv2.imwrite(os.path.join('data_test','zongde.png'),img)
cv2.imshow('frame',img)
cv2.waitKey(0)
# while True:
#     ret,frame = cap.read()
#     if not ret:
#         print("camera can't be opened ")
#         break
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) == ord('q'):
#         break
cap.release()
# cap.destroyAllWindows()