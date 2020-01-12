import cv2
import numpy as np
import pyautogui
import matplotlib.pyplot as plt
from win32api import GetSystemMetrics

def getCord(img,delta):
    x0,x1,y0,y1=0,0,0,0
    w,h =GetSystemMetrics(0),GetSystemMetrics(1)
    if(img.x0Cord-delta>=0):
        x0 = img.x0Cord-delta
    else:
        x0 = 0

    if (img.x1Cord + delta <= w):
        x1 = img.x1Cord + delta
    else:
        x1 = w

    if (img.y0Cord - delta >= 0):
        y0 = img.y0Cord - delta
    else:
        y0 = 0

    if (img.y1Cord + delta <= h):
        y1 = img.y1Cord + delta
    else:
        y1 = h

    return x0,x1,y0,y1


def tempScreenShot(img):
    x0,x1,y0,y1 = getCord(img,50)
    myScreenshot = pyautogui.screenshot()
    myScreenshot = myScreenshot.crop((x0, y0, x1, y1))
    return myScreenshot

def photoRec(templatePath,photo, template):
    photo = np.array(photo)
    gray_img = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(templatePath + "ScreenShots\\" + template.img,0)
    w, h = template.shape[::-1]
    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.8)
    flag=0
    for pt in zip(*loc[::-1]):
        cv2.rectangle(photo, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
        flag = 1



    if (flag==1):
        return True
    else:
        return False
