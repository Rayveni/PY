from os import environ,pathsep
import requests
from PIL import Image
from collections import Counter
from io import BytesIO
import numpy as np
import cv2
from pytesseract import image_to_string
class ocr:
    def __init__(self,tessaract_path=r'C:\Program Files (x86)\Tesseract-OCR'):
        environ["PATH"] += pathsep + tessaract_path
		
    @staticmethod
    def download_image(url):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img        
		
    @staticmethod
    def convert_RGB_to_BGRarray(img):
        img_array=np.array(img.convert('RGB'))
        return img_array[:, :, ::-1]

    @staticmethod
    def elim_noise(img,thresh= (175,255),blur= False,dilate = (1,1),canny=(100,200),erode=(1,1)):
         # Конвертируем цветное изображение в монохромное 
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if thresh:
            img_gray = cv2.threshold(img_gray, *thresh, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        #Otsu algorithm to choose the optimal threshold value; при данном флаге  175, 255, cv2.THRESH_BINARY игнорируются
        
        if blur:
            img_gray = cv2.medianBlur(img_gray, 3)

        img_gray = cv2.bitwise_not(img_gray)

        if dilate:
            #img_gray = cv2.bitwise_not(img_gray)
            kernel = np.ones(dilate, np.uint8)
            img_gray = cv2.dilate(img_gray, kernel, iterations=1) #cv2.morphologyEx(img_gray, cv2.MORPH_DILATE, kernel)
            #img_gray = cv2.bitwise_not(img_gray)
        if erode:
            kernel=np.ones(erode, np.uint8)
            img_gray=cv2.erode(img_gray, kernel, iterations=1)   
        if canny:
            img_gray=cv2.Canny(img_gray, *canny)
        # Детектируем ребра (фильтр канни)
        return img_gray
    
    def recognize_img(self,img):
        bgr_img=self.convert_RGB_to_BGRarray(img)
        img_arr=(self.elim_noise(bgr_img,blur= False,dilate=(2,1) ,canny=False),
                 self.elim_noise(bgr_img,blur= False,dilate=(1,1) ,canny=False),
                 self.elim_noise(bgr_img,blur= False,dilate=(2,2) ,canny=False),
                 self.elim_noise(bgr_img,blur= False,dilate=(1,2) ,canny=False)
                )
        recognize_f=lambda image:image_to_string(image,lang='eng')
        text_arr=list(map(recognize_f,img_arr))
        return text_arr
    
    def text_from_image(self,img):
        text_arr=[el for el in self.recognize_img(img) if el!='' and all(map(str.isupper, el))]
        most_common=Counter(text_arr)
        if len(most_common)==0:
            return False,None,img
        
        most_common2top=most_common.most_common(2)
        freq=most_common.most_common(1)[0]
        if  len(most_common2top)==2 and  most_common2top[0][1]==most_common2top[1][1]:
            return most_common,most_common2top
            res=False,[k for k,v in most_common  if v==freq[1]],img
        else:
            res=True,freq[0],None
        
        return res