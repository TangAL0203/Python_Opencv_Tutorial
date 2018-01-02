#-*- coding:utf-8 -*-
import cv2
video_path = "/media/tsq/home/Ubuntu/video/passerby.avi"
cap = cv2.VideoCapture(video_path)
cv2.namedWindow("Video FPS Display")
while(1):
    t = cv2.getTickCount()
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    if(cap.isOpened()):
        flag,img = cap.read()
        t = (float)(cv2.getTickCount() - t) / cv2.getTickFrequency()
        fps = 1.0 / t
        cv2.putText(img,
                "FPS: %.2f" % float(fps),
                (5,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),2,cv2.LINE_AA)
        cv2.imshow("Video FPS Display", img)
    else:
        print("No Video Input!")
        break
        
# opencv doc about cv2.putText func: 
# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_drawing_functions/py_drawing_functions.html?highlight=puttext
