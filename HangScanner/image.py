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


class Contour:
    def __init__(self, Image):
        self.img = Image
        self.imgContours = self.img.image.copy()
        self.contours = self.findContours()

    def findContours(self):
        contours, _ = cv2.findContours(self.img.imageThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours


class BiggestContour(Contour):
    def __init__(self, Image):
        super().__init__(Image)
        self.imgBigContour = self.img.image.copy()
        self.biggest, self.max_area = self.biggestContour()

    def biggestContour(self):
        '''
            Tìm vùng có đường viền kín lớn nhất
            Ý tưởng: tính vùng có diện tích lớn nhất (area) và có đường vẽ kín (approx).
        '''
        area_lst = [cv2.contourArea(i) for i in self.contours] #Liệt kế tất cả kích thước của contour
        area_argsorted = sorted(range(len(area_lst)), key=lambda k: area_lst[k], reverse=True) #Sắp xếp thứ tự theo index của kích thước contour
        approx = [cv2.approxPolyDP(i, 0.02 * cv2.arcLength(i, True), True) for i in self.contours] 
        for i in area_argsorted: 
            if len(approx[i]) == 4: #Tìm những approx có 4 đỉnh 
                return approx[i], area_lst[i] 
        return np.array([]), 0

    def drawRectangle(self,thickness):
        cv2.line(self.imgBigContour, (self.biggest[0][0][0], self.biggest[0][0][1]), (self.biggest[1][0][0], self.biggest[1][0][1]), (0, 255, 0), thickness)
        cv2.line(self.imgBigContour, (self.biggest[0][0][0], self.biggest[0][0][1]), (self.biggest[2][0][0], self.biggest[2][0][1]), (0, 255, 0), thickness)
        cv2.line(self.imgBigContour, (self.biggest[3][0][0], self.biggest[3][0][1]), (self.biggest[2][0][0], self.biggest[2][0][1]), (0, 255, 0), thickness)
        cv2.line(self.imgBigContour, (self.biggest[3][0][0], self.biggest[3][0][1]), (self.biggest[1][0][0], self.biggest[1][0][1]), (0, 255, 0), thickness)
        return self.imgBigContour

    def reorder(self):
        self.biggest = self.biggest.reshape((4, 2))
        myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
        add = self.biggest.sum(1)
    
        myPointsNew[0] = self.biggest[np.argmin(add)]
        myPointsNew[3] =self.biggest[np.argmax(add)]
        diff = np.diff(self.biggest, axis=1)
        myPointsNew[1] =self.biggest[np.argmin(diff)]
        myPointsNew[2] = self.biggest[np.argmax(diff)]
        return myPointsNew

    def DrawBiggestContour(self):
        self.biggest = self.reorder()
        cv2.drawContours(self.imgBigContour, self.biggest, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
        self.imgBigContour = self.drawRectangle(2)
        return self.imgBigContour

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
