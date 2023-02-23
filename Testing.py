from PIL import Image
import cv2 as cv
import os
import pandas as pd
import pytesseract
import re
import PyPDF2
import docx
import openpyxl
import numpy as np

url="MicrosoftTeams-image (1).png"

#Creating directory fro file uploading
path=os.getcwd()
UploadDir=os.path.join(path,"UploadDir")
if not os.path.isdir(UploadDir):
    os.mkdir(UploadDir)

#Creating directory for save extracted textfile
OCRDir=os.path.join(path,"OCRDir")
if not os.path.isdir(OCRDir):
    os.mkdir(OCRDir)

#file path
file=os.path.join(UploadDir,url)
print(file)
fileExtension=os.path.split(file)[1].split(".")[1]

#open a text file for writing extracted text
textFile=open(os.path.join(OCRDir,"file.txt"),"w",encoding="utf-8")

#main processing function
def process(file,fileExtension):
    bool = checkingForImage(fileExtension)
    
    if bool:
        extractTextByOCR(file)
        return 

    
    if(fileExtension=="pdf"):
        extractTextFromPDF(file)

    if(fileExtension=="docx"):
        extractTextFromDOCX(file)
    
    if(fileExtension=="xlsx"):
        extractTextFromExcel(file)
            
#checking for image or other file formats(pdf,doc,exl,etc)
def  checkingForImage(fileExtension):
    imageString="jpgpngtifftifbmpwebppbmpgmppmxpmxbm"
    search=re.search(fileExtension.lower(),imageString)
    if search:
        return True
    else:
        return False

#function for extracting text from images with pytesseract
def extractTextByOCR(file):
    global textFile
    image=cv.imread(file)

    grayImage=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    cv.imwrite(os.path.join(OCRDir,"grayImage.png"),grayImage)
    kernel = np.ones((5,5),np.uint8)

    dialation = cv.dilate(grayImage,kernel,iterations=1)
    cv.imwrite(os.path.join(OCRDir,"dialation.png"),dialation)

    erosion = cv.erode(dialation,kernel,iterations = 1)
    cv.imwrite(os.path.join(OCRDir,"erosion.png"),erosion)
    
    #bluredImage=cv.GaussianBlur(dialation,(3,3),0)
    #cv.imwrite(os.path.join(OCRDir,"bluredImage.png"),bluredImage)
    #thresholdImage=cv.threshold(grayImage,50,255,cv.THRESH_BINARY)[1]
    #thresholdImage=cv.adaptiveThreshold(erosion,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,3,2)
    #thresholdImage=cv.threshold(thresholdImage_,10,255,cv.THRESH_BINARY)[1]
    #thresholdImage=cv.adaptiveThreshold(bluredImage,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,21,2)
    #thresholdImage=cv.threshold(erosion,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)[1]
    
    #cv.imwrite(os.path.join(OCRDir,"fimage.png"),thresholdImage)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
    stringtext=pytesseract.image_to_string(erosion, lang=("eng"))
    textFile.write(stringtext)
    textFile.close()


#extracting readable text from pdf n write it on textfile
def extractTextFromPDF(file):
    global textFile
    pdfFile=open(file,"rb")
    pdfFileReader=PyPDF2.PdfReader(pdfFile)
    
    pageList=pdfFileReader.pages
    for page in pageList:
        text=page.extract_text()
        textFile.write(text)
    textFile.close()
    
#extracting readable text from worddoc n write it on textfile
def extractTextFromDOCX(file):
    global textFile
    docFile=open(file,"rb")
    newdoc=docx.Document(docFile)
    paraList=newdoc.paragraphs
    
    for paragraph in paraList:
        textFile.write(paragraph.text)
        textFile.write("\n")
    textFile.close()
#extracting readable text from excel sheet n write it on textfile
def extractTextFromExcel(file):
    global textFile
    dataFrame=pd.read_excel(file)
    for i,j in dataFrame.iterrows():
        textFile.write(str(i)+" "+str(j))
        textFile.write("\n")
    textFile.close()

process(file,fileExtension)