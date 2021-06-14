import cv2
import numpy as np

class Image:
    def __init__(self, width, height, cap, Blur_ksize, sigmaX, thres, kernel, pathImage, webcamFeed = True):
        self.width = width
        self.height = height
        self.image = self.load_img(cap, pathImage, webcamFeed)
        self.imageGray = self.Gray()
        self.imageBlur = self.GaussianBlur(Blur_ksize, sigmaX)
        self.imageBlank = self.Blank()
        self.imageThreshold = self.Threshold(thres, kernel)

    def load_img(self, cap, pathImage, webCamFeed):
        if webCamFeed:
            _, self.image = cap.read()
        else:
            self.image = cv2.imread(pathImage)
        self.image = cv2.resize(self.image, (self.width, self.height))
        return self.image

    def Gray(self):
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def GaussianBlur(self, kernel, sigmaX):
        return cv2.GaussianBlur(self.imageGray, kernel, sigmaX)

    def Blank(self):
        return np.zeros((self.height, self.width, 3), np.uint8)

    def Threshold(self, thres, kernel):
        imgThreshold = cv2.Canny(self.imageBlur,thres[0],thres[1]) # APPLY CANNY BLUR
        imgDial = cv2.dilate(imgThreshold, kernel, iterations=2) # APPLY DILATION
        imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION
        return imgThreshold
