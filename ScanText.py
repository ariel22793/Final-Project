import pytesseract
import os
import PIL
from tkinter import *
from tkinter import messagebox
import sys
import tkinter.ttk as ttk
# import tkinter.filedialog
import wget
import time
from tkinter import filedialog
from multiprocessing import Process
import webbrowser
import ImgRecog
import matplotlib.pyplot as plt
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def check_if_instaled():
    if os.path.isfile(r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        pass
    else:
        MsgBox = messagebox.askyesno("Error","To run scan option, Tesseract-OCR must be installed. Do you want to download it?")
        print(MsgBox)
        if MsgBox == True:
            webbrowser.open('https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe', new=2)
        else:
            exit()

def scan_text(path_to_image):
    check_if_instaled()
    image = PIL.Image.open(path_to_image)
    text = pytesseract.image_to_string(image)
    return text

def scan_text_and_compare(image, text_to_compare):
    check_if_instaled()
    threshold = 100
    image2 = image.point(lambda x : 255 if (x<=threshold) else 0)
    image3 = image.point(lambda x : 0 if (x<=threshold) else 255)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(image)
    text2 = pytesseract.image_to_string(image2)
    text3 = pytesseract.image_to_string(image3)

    if text == text_to_compare or text2 == text_to_compare or  text3 == text_to_compare :
        return True
    else:
        return False



if __name__ == '__main__':
    x = scan_text_and_compare(r'C:\Users\AZ\PycharmProjects\Final-Project\img\test.png', '123456')
    print(x)