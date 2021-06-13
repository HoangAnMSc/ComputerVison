from config import *

from utils import *
from TypeImg import *
from Contours import *
from ImgWarp import *
bar=Trackbars()

imgblack=None
while True:
    if webCamFeed:
        success, img = cap.read()
    else:
        img = cv2.imread(pathImage)
    img=cv2.resize(img, (widthImg, heightImg))
    
    Img=TypeImage(img) #Ảnh gốc 
    #Ảnh imgThreshold
    imgThreshold=Img.Create_imgThreshold(bar) 
    #ảnh contour
    contours,biggest,max_area = Img.Find_Biggest_Contour()
    imgContour=ImgContours(img,imgThreshold,contours,biggest,max_area)
    image_contour=imgContour.Draw_Contours()

    if biggest.size !=0:
        #ảnh biggest
        try:
            imgBigContour=imgContour.Draw_Biggest_Contours()

            warp = WrapImg(img,imgThreshold,contours,biggest,max_area)
            WrapImgColor=warp.Create_WarpColor()
            imgWarpGray=warp.Create_WarpGray()
            imageArray = [[img,Img.Create_imgGray(),imgThreshold,image_contour],
                            [imgBigContour,WrapImgColor, imgWarpGray,imgWarpGray]]
        except:
            imageArray = [[img,Img.Create_imgGray(),imgThreshold,image_contour],
                    [imgBlank,imgBlank, imgBlank,imgBlank]]
            
    else:
        
        imageArray = ([img,Img.Create_imgGray(),imgThreshold,image_contour],
                    [imgBlank,imgBlank, imgBlank,imgBlank])
    lables = [["Original","Gray","Threshold","Contours"],
            ["Biggest Contour","Warp Prespective","Warp Gray","Adaptive Threshold"]]
    stackedImage = stackImages(imageArray,0.75,lables)
    cv2.imshow("Result",stackedImage)
    cv2.waitKey(1)
    

