import cv2
import numpy as np

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

