from PIL import Image
import cv2 as cv
import os
import pandas as pd
import pytesseract
import re
import PyPDF2
import docx
import docxpy
import openpyxl
import numpy as np




stringDic={}

#main processing function
def process(filepath,fileExtension):
    bool = checkingForImage(fileExtension)
    
    if bool:
        return extractTextByOCR(filepath) 

    if(fileExtension=="pdf"):
        extractTextFromPDF(filepath)

    if(fileExtension=="docx"):
       return extractTextFromDOCX(filepath)
    
    if(fileExtension=="xlsx"):
        extractTextFromExcel(filepath)
            
#checking for image or other filepath formats(pdf,doc,exl,etc)
def  checkingForImage(fileExtension):
    imageString="jpgpngtifftifbmpwebppbmpgmppmxpmxbm"
    search=re.search(fileExtension.lower(),imageString)
    if search:
        return True
    else:
        return False

#function for extracting text from images with pytesseract
def extractTextByOCR(filepath):
    image=cv.imread(filepath)
    grayImage=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    
    #kernel = np.ones((5,5),np.uint8)
    #dialation = cv.dilate(grayImage,kernel,iterations=1)
    #erosion = cv.erode(dialation,kernel,iterations = 1)
   
    
    #bluredImage=cv.GaussianBlur(dialation,(3,3),0)
    #cv.imwrite(os.path.join(OCRDir,"bluredImage.png"),bluredImage)
    #thresholdImage=cv.threshold(grayImage,50,255,cv.THRESH_BINARY)[1]
    #thresholdImage=cv.adaptiveThreshold(erosion,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,3,2)
    #thresholdImage=cv.threshold(thresholdImage_,10,255,cv.THRESH_BINARY)[1]
    #thresholdImage=cv.adaptiveThreshold(bluredImage,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,21,2)
    #thresholdImage=cv.threshold(erosion,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)[1]
    
    #cv.imwrite(os.path.join(OCRDir,"fimage.png"),thresholdImage)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
    stringtext=pytesseract.image_to_string(grayImage, lang=("eng"))
    return stringtext

#extracting readable text from pdf n write it on textfile
def extractTextFromPDF(filepath):
    
    pdfFile=open(filepath,"rb")
    pdfFileReader=PyPDF2.PdfReader(pdfFile)
    stringText=""
    pageList=pdfFileReader.pages
    for page in pageList:
        text=page.extract_text()
        stringText=stringText+text
    return stringText
    
#extracting readable text from worddoc n write it on textfile
def extractTextFromDOCX(filepath):
    stringText=""
    docFile=open(filepath,"rb")
    newdoc=docx.Document(docFile)
    paraList=newdoc.paragraphs
    for paragraph in paraList:
        stringText=stringText+paragraph.text
    return stringText
    
def extractTextFromDOCXwithdocxpy(filepath):
    return docxpy.process(filepath)        
#extracting readable text from excel sheet n write it on textfile
def extractTextFromExcel(filepath):
    global textFile
    dataFrame=pd.read_excel(filepath)
    stringText=""
    for i,j in dataFrame.iterrows():
        stringText=stringText+str(i)+" "+str(j)
        
    return stringText
