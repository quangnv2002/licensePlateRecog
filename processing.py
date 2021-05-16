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

window = Tk()
window.title("Output")
window.geometry("400x100")
window.resizable(False,False)
window.iconbitmap("Image/UET-logo.ico")

bg_loading = Image.open("Image/background.png")
bg_render = ImageTk.PhotoImage(bg_loading)
bg = Label(window,image=bg_render)
bg.place(x=0,y=0)
def cut(path):
    img = cv2.imread(path)
    cv2.imshow('Input',img)
    #img = cv2.resize(img, (0, 0), fx=2, fy=2)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    contours, h = cv2.findContours(thresh, 1, 2)
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
    print('Cut')
    cv2.imshow('Image Cut',image)
    return image

def analysis(image):
    reader = easyocr.Reader(['en', 'ch_tra'])
    result = reader.readtext(image)
    text = ''
    for res in result:
        text+= res[1] + ' '
    print('License Plate Information : ')
    print(text)
    return text

path = 'licenseplateImg/7.png'
img = cut(path)
text = analysis(img)
txt = Label(window,text = 'License Plate :',font=("Impact",10,"italic"),fg='#A60F1C',bg='#FDBFC0')
txt.place(x=0,y=0)
lbl = Label(window, text=text,font=("Impact",30,"bold"),fg='#A60F1C',bg='#FDBFC0')
lbl.pack()

window.mainloop()
cv2.waitKey()
