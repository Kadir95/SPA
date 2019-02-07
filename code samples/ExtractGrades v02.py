import os
from sys import exit
from PyPDF2 import PdfFileReader, PdfFileWriter

from pdf2image import convert_from_path, convert_from_bytes

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
 
import cv2
import numpy as np
from pytesseract import image_to_string
import glob, os

import pandas as pd
from nolearn.dbn import DBN
##import timeit

import cv2
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np


def getnumber(im):
    os.chdir("C:\Python27\GDrive")
    clf,pp = joblib.load("digits_cls1.pkl")

    # Read the input image 
    # im = cv2.imread("unnamed1.jpg")

    # Convert to grayscale and apply Gaussian filtering
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

    # Threshold the image
    ret, im_th = cv2.threshold(im_gray, 220, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the image
    # _,ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    _,ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Get rectangles contains each contour
    rects = [cv2.boundingRect(ctr) for ctr in ctrs]
    number=''

    maxrect3=0
    for rect in rects:
        if rect[3]>=maxrect3:
            maxrect3=rect[3]
            maxrect=rect


            
    #for rect in rects:
    rect=maxrect
    if True:
        # print(' '.join(map(str, rect)))
        if rect[3]>20:
            # Draw the rectangles
            cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 1) 

            # Make the rectangular region around the digit
            leng = int(rect[3] * 1.6)

            roi = np.zeros((leng,leng), np.uint8)
            small_img = im_th[int(rect[1]):int(rect[1]+rect[3]), int(rect[0]):int(rect[0]+rect[2])]
            y_offset=leng // 2 - rect[3] // 2    
            x_offset=leng // 2 - rect[2] // 2    
            roi[y_offset:y_offset+rect[3], x_offset:x_offset+rect[2]] = small_img            

            # pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
            # pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
            # roi = im_th[pt1:pt1+leng, pt2:pt2+leng]

            # Resize the image
            roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
            roi = cv2.dilate(roi, (3, 3))

            # Calculate the HOG features
            roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
            roi_hog_fd = pp.transform(np.array([roi_hog_fd], 'float64'))
            # Pridict digit
            nbr = clf.predict(roi_hog_fd)
            cv2.putText(im, str(int(nbr[0])), (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)
            print nbr
            
            number = number + str(int(nbr[0]))

    print(number) 
    #cv2.namedWindow("Resulting Image with Rectangular ROIs", cv2.WINDOW_NORMAL)
    im_resized = cv2.resize(im, None, fx=0.3, fy=0.3)
    #cv2.imshow("Resulting Image with Rectangular ROIs", roi)
    #cv2.waitKey(5)
    #cv2.destroyAllWindows()
    return number     




os.chdir("C:\Python27\GDrive\Exams")
for file in glob.glob("*.pdf"):
    print file
    with open(file,"r") as f:
        firstfile=True
        images = convert_from_path(file)

        # Convert to cv2 and resize        
        im = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2BGR)
        im_resized = cv2.resize(im, None, fx=0.3, fy=0.3)
        
        # Select ROI
        if firstfile:
            r = cv2.selectROI(im_resized)
            print(' '.join(map(str, r)))
            r = [int(x*10/3) for x in r]
            print(' '.join(map(str, r)))
            

        firstfile=False
            
        # Crop image
        imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        print('number= {}'.format(getnumber(imCrop)))

print "All files have been processed"






         
