import cv2 
import numpy as np
from utils import *
from config import *
from TypeImg import *
class ImgContours(TypeImage):
    def __init__(self,img,imgThreshold=None,contours=None,biggest=None,max_area=None):
        super().__init__(img,imgThreshold,contours,biggest,max_area)
        imgContours=self.img.copy()
        cv2.drawContours(imgContours, self.contours, -1, (0, 255, 0), 10)
        self.imgContours=imgContours
        self.imgBigContour=self.img.copy()
    def Draw_Contours(self):
        return self.imgContours
    def Repair_Biggest_Contour(self):
        myPoints = self.biggest.reshape((4, 2))
        myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
        add = myPoints.sum(1) #Tính toán cộng
        diff = np.diff(myPoints, axis=1) #Tính hiệu rời rạc 
        temp=[np.argmin(add),np.argmin(diff),np.argmax(diff),np.argmax(add)]
        for i in range(len(temp)):
            myPointsNew[i] = myPoints[temp[i]]
        
        self.biggest=myPointsNew
    def Draw_Biggest_Contours(self):
        self.Repair_Biggest_Contour()
        cv2.drawContours(self.imgBigContour, self.biggest, -1, (0, 255, 0), 20)
        self.imgBigContour=drawRectangle(self.imgBigContour,self.biggest,2)
        return self.imgBigContour

        
