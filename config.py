import numpy as np

# Image
path_img = '3.jpg'
webcamFeed = False
heightImg = 640
widthImg  = 480


# Blur Image
ksize = (5,5)
sigmaX = 1 

# Threshold
kernel = np.ones((5, 5))