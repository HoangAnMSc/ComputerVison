import cv2
import numpy as np
webCamFeed = True
heightImg = 640
widthImg  = 480
pathImage = "2.jpg"
cap=cv2.VideoCapture(0)
cap.set(10,160)

imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8) 
labels = [["Original","Gray","Threshold","Contours"],
            ["Biggest Contour","Warp Prespective","Warp Gray","Adaptive Threshold"]]