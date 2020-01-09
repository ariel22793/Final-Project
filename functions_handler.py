import pyautogui

def click_handle(img):
    exist = 1
    x = (img.x1Cord + img.x0Cord) / 2
    y = (img.y1Cord + img.y0Cord) / 2
    if(exist == 1):
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

