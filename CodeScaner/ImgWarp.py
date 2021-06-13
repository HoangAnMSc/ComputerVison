import TypeImg
from TypeImg import *
class WrapImg(TypeImage):
    def __init__(self,img,imgThreshold=None,contours=None,biggest=None,max_area=None):
        super().__init__(img,imgThreshold,contours,biggest,max_area)
        self.imgWarpColored=self.imgWarpGray =None
    def Repair_Biggest_Contour(self):
        myPoints = self.biggest.reshape((4, 2))
        myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
        add = myPoints.sum(1) #Tính toán cộng
        diff = np.diff(myPoints, axis=1) #Tính hiệu rời rạc 
        temp=[np.argmin(add),np.argmin(diff),np.argmax(diff),np.argmax(add)]
        for i in range(len(temp)):
            myPointsNew[i] = myPoints[temp[i]]
        self.biggest=myPointsNew       
    def Create_WarpColor(self):
        self.Repair_Biggest_Contour()
        pts1 = np.float32(self.biggest) # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2) #trả về phép biến đổi phối cảnh 3x3 cho 4 cặp điểm tương ứng. Từ 4 điểm ảnh gốc tạo 4 điểm cho ảnh đích 
        imgWarpColored = cv2.warpPerspective(self.img, matrix, (widthImg, heightImg)) #Áp dụng một phép chuyển đổi phối cảnh cho một hình ảnh
        #Remove 20 pixels
        imgWarpColored=imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
        imgWarpColored = cv2.resize(imgWarpColored,(widthImg,heightImg)) 
        self.imgWarpColored= imgWarpColored
        return self.imgWarpColored
    def Create_WarpGray(self):
        imgWarpGray = cv2.cvtColor(self.imgWarpColored,cv2.COLOR_BGR2GRAY)
        imgAdaptiveThre= cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
        imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
        imgAdaptiveThre=cv2.medianBlur(imgAdaptiveThre,3)
        self.imgWarpGray=imgWarpGray
        return self.imgWarpGray        

