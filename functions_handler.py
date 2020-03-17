import pyautogui
import ImgRecog
import time




def repeat_handle(repeatTime,functions,path):
    functionNum = 0
    for i in range(repeatTime):
        for func in functions:
            if ('(' in func.name and func.name[:func.name.index('(')] == 'Repeat'):
                functionNum += repeat_handle(func.extra.time, func.extra.functions,path) + 3
            elif (func.name == 'Left-Click'):
                time.sleep(0.3)
                left_click_handle(func.img, path)
                functionNum += 1
            elif (func.name == 'Exist'):
                exist_handle(func.img)
                functionNum += 1
            elif (func.name == 'NotExist'):
                not_exist_handle(func.img)
                functionNum += 1
            elif (func.name == 'Double-Click'):
                double_click_handle(func.img,path)
                functionNum += 1
            elif (func.name == 'Right-Click'):
                right_click_handle(func.img,path)
                functionNum += 1
            elif (func.name == 'Sleep'):
                right_click_handle(func.extra.time)
                functionNum += 1
    return functionNum/repeatTime

def sleep_handle(timeDelay):
    time.sleep(timeDelay)

def left_click_handle(template,path):
    screenShot = ImgRecog.tempScreenShot(template)

    exist = ImgRecog.photoRec(path,screenShot,template)
    x = (template.x1Cord + template.x0Cord) / 2
    y = (template.y1Cord + template.y0Cord) / 2
    print(exist)
    if(exist == True):
        pyautogui.click(x,y,duration=0.5)

def double_click_handle(template,path):
    screenShot = ImgRecog.tempScreenShot(template)

    exist = ImgRecog.photoRec(path,screenShot,template)
    x = (template.x1Cord + template.x0Cord) / 2
    y = (template.y1Cord + template.y0Cord) / 2
    print(exist)
    if(exist == True):
        pyautogui.doubleClick(x,y,duration=0.5)

def right_click_handle(template,path):
    screenShot = ImgRecog.tempScreenShot(template)

    exist = ImgRecog.photoRec(path,screenShot,template)
    x = (template.x1Cord + template.x0Cord) / 2
    y = (template.y1Cord + template.y0Cord) / 2
    print(exist)
    if(exist == True):
        pyautogui.rightClick(x,y,duration=0.5)

def exist_handle(img):
    exist = 1
    if(exist == 1):
        return True
    else:
        return False

def not_exist_handle(img):
    exist = 1
    if(exist == 1):
        return False
    else:
        return True

