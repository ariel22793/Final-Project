import pyautogui
import ImgRecog
import time





def repeat_handle(fatherFunction,path):
    repeatTime = fatherFunction.extra.time
    childrenFunction = fatherFunction.extra.functions
    functionNum = 0
    for i in range(repeatTime):
        for func in childrenFunction:
            if (func.name == 'Repeat'):
                functionNum += repeat_handle(func,path) + 3
            elif (func.name == 'Left-Click'):
                left_click_handle(func.img, path)
                functionNum += 1
            elif (func.name == 'If-Exist'):
                exist, tempFunctionNum = exist_handle(func, path)
                functionNum += tempFunctionNum
                ifExistFlag = exist
            elif (func.name == 'If-Not-Exist'):
                exist, tempFunctionNum = not_exist_handle(func, path)
                functionNum += tempFunctionNum
                ifExistFlag = exist
            elif (func.name == 'Double-Click'):
                double_click_handle(func.img)
                functionNum += 1
            elif (func.name == 'Else' and not ifExistFlag):
                functionNum += else_handle(func, path)
            elif (func.name == 'Right-Click'):
                right_click_handle(func.img)
                functionNum += 1
            elif (func.name == 'Sleep'):
                sleep_handle(func.extra.time)
                functionNum += 1
            elif (func.name == 'Insert-Input'):
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

def exist_handle(fatherFunction,path):
    childrenFunctions = fatherFunction.extra.functions
    template = fatherFunction.img
    ifExistFlag = True
    screenShot = ImgRecog.tempScreenShot(template)
    exist = ImgRecog.photoRec(path, screenShot, template)
    functionNum = 0
    if(exist == True):
        for func in childrenFunctions:
            if(func.father[0] == fatherFunction.id):
                if (func.name == 'Repeat'):
                    functionNum += repeat_handle(func, path) + 3
                elif (func.name == 'Left-Click'):
                    left_click_handle(func.img, path)
                    functionNum += 1
                elif (func.name == 'If-Exist'):
                    exist,tempFunctionNum = exist_handle(func,path)
                    functionNum += tempFunctionNum
                    ifExistFlag = exist
                elif (func.name == 'If-Not-Exist'):
                    exist, tempFunctionNum = not_exist_handle(func, path)
                    functionNum += tempFunctionNum
                    ifExistFlag = exist
                elif (func.name == 'Double-Click'):
                    double_click_handle(func.img)
                    functionNum += 1
                elif (func.name == 'Else' and not ifExistFlag):
                    functionNum += else_handle(func, path)
                elif (func.name == 'Right-Click'):
                    right_click_handle(func.img,path)
                    functionNum += 1
                elif (func.name == 'Sleep'):
                    sleep_handle(func.extra.time)
                    functionNum += 1
                elif (func.name == 'Insert-Input'):
                    right_click_handle(func.extra.time)
                    functionNum += 1

    return exist,functionNum

def not_exist_handle(fatherFunction,path):
    childrenFunctions = fatherFunction.extra.functions
    template = fatherFunction.img
    ifExistFlag = True
    screenShot = ImgRecog.tempScreenShot(template)
    exist = ImgRecog.photoRec(path, screenShot, template)
    if (exist == False):
        functionNum = 0
        for func in childrenFunctions:
            if (func.name == 'Repeat'):
                functionNum += repeat_handle(func, path) + 3
            elif (func.name == 'Left-Click'):
                left_click_handle(func.img, path)
                functionNum += 1
            elif (func.name == 'If-Exist'):
                exist, tempFunctionNum = exist_handle(func, path)
                functionNum += tempFunctionNum
                ifExistFlag = exist
            elif (func.name == 'If-Not-Exist'):
                exist, tempFunctionNum = not_exist_handle(func, path)
                functionNum += tempFunctionNum
                ifExistFlag = exist
            elif (func.name == 'Double-Click'):
                double_click_handle(func.img)
                functionNum += 1
            elif (func.name == 'Else' and not ifExistFlag):
                functionNum += else_handle(func, path)
            elif (func.name == 'Right-Click'):
                right_click_handle(func.img)
                functionNum += 1
            elif (func.name == 'Sleep'):
                sleep_handle(func.extra.time)
                functionNum += 1
            elif (func.name == 'Insert-Input'):
                right_click_handle(func.extra.time)
                functionNum += 1

    return exist, functionNum

def else_handle(fatherFunction,path):
    childrenFunctions = fatherFunction.extra.functions
    ifExistFlag = True
    functionNum = 0
    for func in childrenFunctions:
        if (func.name == 'Repeat'):
            functionNum += repeat_handle(func, path) + 3
        elif (func.name == 'Left-Click'):
            left_click_handle(func.img, path)
            functionNum += 1
        elif (func.name == 'If-Exist'):
            exist, tempFunctionNum = exist_handle(func, path)
            functionNum += tempFunctionNum
            ifExistFlag = exist
        elif (func.name == 'If-Not-Exist'):
            exist, tempFunctionNum = not_exist_handle(func, path)
            functionNum += tempFunctionNum
            ifExistFlag = exist
        elif (func.name == 'Double-Click'):
            double_click_handle(func.img)
            functionNum += 1
        elif (func.name == 'Else' and not ifExistFlag):
            functionNum += else_handle(func, path)
        elif (func.name == 'Right-Click'):
            right_click_handle(func.img)
            functionNum += 1
        elif (func.name == 'Sleep'):
            sleep_handle(func.extra.time)
            functionNum += 1
        elif (func.name == 'Insert-Input'):
            right_click_handle(func.extra.time)
            functionNum += 1

    return functionNum