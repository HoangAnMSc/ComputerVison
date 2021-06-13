from config import *

class TypeImage:
    def __init__(self, img,imgThreshold=None,contours=None,biggest=None,max_area=None):
        self.img = img
        self.imgGray=None
        self.imgThreshold=imgThreshold
        self.contours=contours
        self.biggest=biggest
        self.max_area=max_area
    def Create_imgGray(self): #ảnh Xám
        self.imgGray =  cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY) 
        return self.imgGray
    def Create_imgThreshold(self,bar):
        self.Create_imgGray()
        imgBlur = cv2.GaussianBlur(self.imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR (làm giảm nhiễu)
        thres=bar.Edit__Track()
        imgThreshold=cv2.Canny(imgBlur,thres[0],thres[1])
        kernel = np.ones((5, 5))
        imgDial = cv2.dilate(imgThreshold, kernel, iterations=2) #  hình ảnh bị đứt nét có thể giúp nối liền ảnh lạ
        imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # đối tượng trở nên mịn hơn
        self.imgThreshold=imgThreshold
        return  self.imgThreshold #Trả về cạnh 
    def Find_Biggest_Contour(self):
        test=self.img.copy()
        contours, hierarchy = cv2.findContours(self.imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.contours=contours
        c = max(self.contours, key = lambda x: cv2.contourArea(x) if cv2.contourArea(x)>5000 and len(cv2.approxPolyDP(x, 0.02 * cv2.arcLength(x, True), True))==4 else  -cv2.contourArea(x) )
        biggest,max_area= cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True),cv2.contourArea(c)
        self.biggest=biggest
        self.max_area=   max_area
        return contours,biggest,max_area


