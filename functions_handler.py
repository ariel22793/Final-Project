import pyautogui
import ImgRecog






def left_click_handle(template,path):
    screenShot = ImgRecog.tempScreenShot(template)

    exist = ImgRecog.photoRec(path,screenShot,template)
    x = (template.x1Cord + template.x0Cord) / 2
    y = (template.y1Cord + template.y0Cord) / 2
    print(exist)
    if(exist == True):
        pyautogui.click(x,y,duration=0.5)

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

