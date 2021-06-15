import cv2
import numpy as np

class Scanner:
    def __init__(self, Image, BiggestContour):
        self.img = Image
        self.BiggestContour = BiggestContour
        self.imgWarpColored, self.imgWarpGray = self.scanner()
        self.imgAdaptiveThre = self.AdaptiveThre()

    def scanner(self):
        pts1 = np.float32(self.BiggestContour.biggest) # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0],[self.img.width, 0], [0, self.img.height],[self.img.width, self.img.height]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv2.warpPerspective(self.img.image, matrix, (self.img.width, self.img.height))

        #REMOVE 20 PIXELS FORM EACH SIDE 
        imgWarpColored = imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
        imgWarpColored = cv2.resize(imgWarpColored,(self.img.width, self.img.height))

        imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)        
        return imgWarpColored, imgWarpGray

    def AdaptiveThre(self):
        imgAdaptiveThre = cv2.adaptiveThreshold(self.imgWarpGray, 255, 1, 1, 7, 2)
        imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
        imgAdaptiveThre = cv2.medianBlur(imgAdaptiveThre,5)
        return imgAdaptiveThre
