import numpy as np
import cv2
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageTk
import PIL.Image # cài đặt pillow
import PIL.ImageTk
from PIL import Image,ImageTk
import tkinter
from tkinter import *
import easyocr
from PIL import Image,ImageTk

path = 'licenseplateImg/7.png'
img = cv2.imread(path)
#cv2.imshow('input',img)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray',gray)

thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2) #ảnh đen trắng
#cv2.imshow('binary',thresh)

contours,h = cv2.findContours(thresh,1,2)
largest_retangle = [0, 0]
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    if len(approx) == 4:
        area = cv2.contourArea(cnt)
        if area > largest_retangle[0]:
            largest_retangle = [cv2.contourArea(cnt), cnt, approx]

x, y, w, h = cv2.boundingRect(largest_retangle[1])
image = img[y:y + h, x:x + w]
cv2.drawContours(img, [largest_retangle[1]], 0, (0, 255, 255), 8)

#cv2.imshow('contours',img)

#cv2.imshow('crop',image)
image = cv2.resize(image, (0, 0), fx=1.7, fy=1.7)
gray_cr = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray_cr',gray_cr)
gray_cr = cv2.fastNlMeansDenoising(gray_cr)
#cv2.imshow('denoise',gray_cr)

gray_cr = cv2.erode(gray_cr, None, iterations=2)
#cv2.imshow('enrode',gray_cr)
gray_cr = cv2.dilate(gray_cr, None, iterations=3)
#cv2.imshow('enrosion and dilation',gray_cr)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
#cv2.imshow('kernel',kernel)
opening = cv2.morphologyEx(gray_cr, cv2.MORPH_OPEN, kernel, iterations=1)
thresh_cr = cv2.threshold(opening, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#cv2.imshow('binary_cr',thresh_cr)

invert = 255-thresh_cr
cv2.imshow('preprocessing',invert)

# reader = easyocr.Reader(['en', 'ch_tra'])
# result = reader.readtext(invert)
# text = ''
# for res in result:
#     text+= res[1] + ' '
# print('License Plate Information : ')
# print(text)



cv2.waitKey(0)