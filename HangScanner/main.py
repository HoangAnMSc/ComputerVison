import cv2
import numpy as np
from HangScanner import utils
from HangScanner.image import Image
from HangScanner.contours import BiggestContour
from HangScanner.scanner import Scanner
import HangScanner.config as cf
from PIL import Image as image

cap = cv2.VideoCapture(0)
cap.set(10,160)



def RUNNNNNNN(webcamFeed,path_img):
    count=0
    utils.initializeTrackbars()
    while True:
        cf.path_img=path_img
        cf.webcamFeed = webcamFeed
        thres = utils.valTrackbars()
        img = Image(cf.widthImg, cf.heightImg, cap, cf.ksize, cf.sigmaX, thres, cf.kernel, cf.path_img, cf.webcamFeed)
        contour = BiggestContour(img)
        cv2.drawContours(contour.imgContours, contour.contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS

        if contour.biggest.size != 0:
            try:
                contour.imgBigContour = contour.DrawBiggestContour()
                scan = Scanner(img, contour)
                imageArray = ([img.image, img.imageGray, img.imageThreshold, contour.imgContours],
                            [contour.imgBigContour, scan.imgWarpColored, scan.imgWarpGray, scan.imgAdaptiveThre])
            except:
                imageArray = ([img.image, img.imageGray, img.imageThreshold, contour.imgContours],
                        [img.imageBlank, img.imageBlank, img.imageBlank, img.imageBlank])
        else:
            imageArray = ([img.image, img.imageGray, img.imageThreshold, contour.imgContours],
                        [img.imageBlank, img.imageBlank, img.imageBlank, img.imageBlank])
    
        # LABELS FOR DISPLAY
        lables = [["Original","Gray","Threshold","Contours"],
                ["Biggest Contour","Warp Prespective","Warp Gray","Adaptive Threshold"]]
    
        stackedImage = utils.stackImages(imageArray,0.75,lables)
        cv2.imshow("Result",stackedImage)
    
        # SAVE IMAGE WHEN 's' key is pressed
        pressedKey = cv2.waitKey(1) & 0xFF
        if pressedKey == ord('s'):
            cv2.imwrite("Scanned/myImage"+str(count)+".jpg",scan.imgWarpColored)
            
            # Convert to PDF
            image1 = image.open("Scanned/myImage"+str(count)+".jpg")
            im1 = image1.convert('RGB')
            im1.save("Scanned/myImage"+str(count)+".pdf")

            cv2.rectangle(stackedImage, ((int(stackedImage.shape[1] / 2) - 230), int(stackedImage.shape[0] / 2) + 50),
                        (1100, 350), (0, 255, 0), cv2.FILLED)
            cv2.putText(stackedImage, "Scan Saved", (int(stackedImage.shape[1] / 2) - 200, int(stackedImage.shape[0] / 2)),
                        cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 255), 5, cv2.LINE_AA)
            cv2.imshow('Result', stackedImage)
            cv2.waitKey(300)
            count += 1
