import cv2
import numpy as np

def nothing(x):
    pass

class Trackbars:
    def __init__(self):
        cv2.namedWindow("Trackbars")
        cv2.resizeWindow("Trackbars", 360, 180)
        cv2.createTrackbar("Threshold1", "Trackbars", 200,255,nothing)
        cv2.createTrackbar("Threshold2", "Trackbars", 200, 255,nothing)
        self.Threshold1,self.Threshold2=0,52
    def Edit__Track(self):
        self.Threshold1 = cv2.getTrackbarPos("Threshold1", "Trackbars")
        self.Threshold2 = cv2.getTrackbarPos("Threshold2", "Trackbars")
        return self.Threshold1, self.Threshold2

def drawRectangle(img,biggest,thickness):
    cv2.line(img, (biggest[0][0][0], biggest[0][0][1]), (biggest[1][0][0], biggest[1][0][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[0][0][0], biggest[0][0][1]), (biggest[2][0][0], biggest[2][0][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[3][0][0], biggest[3][0][1]), (biggest[2][0][0], biggest[2][0][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[3][0][0], biggest[3][0][1]), (biggest[1][0][0], biggest[1][0][1]), (0, 255, 0), thickness)
    return img
