#import requests
import time
import requests_async as requests
import asyncio
import aiohttp  
import json
from datetime import datetime
import os
from obs import ObsClient
import threading
import schedule
from CharacterExtraction import *  
from datetime import datetime
from pymongo import MongoClient
import shutil



userAuth={'username':'superuser','password':'superuser3dms'}
apiConfig={ "userPortalHost": "http://localhost",# "https://www.docubinet.com"
  "userPortalPort": "5000",
  "enterpriseSearchHost": "http://localhost",#//www.docubinet.com
  "enterpriseSearchPort": "5003"}
huaweiObjectStorageConfig={ 
  "huaweiObsAccessKey": "LZZDXMVWWA8ZTECX26RB",
  "huaweiObsSecreatAccessKey": "8xJElsflfLe0ut2coPsPYlqXEdFbJsR6qoroJmio",
  "huaweiObsServerEndpoint": "https://obs.ap-southeast-3.myhuaweicloud.com",
  "bucketName": "001-docubinet",
}
baseUrl=apiConfig["userPortalHost"]+":"+apiConfig["userPortalPort"]
OCRtype="2"
fileList=[]

path=os.getcwd()
UploadDir=os.path.join(path,"UploadDir")
if not os.path.isdir(UploadDir):
    os.mkdir(UploadDir)
""" 
async def mainMethod():
    schedule.every(24).hours.do()
    schedule.every(5).seconds.do()
    while True:
        schedule.run_pending()
"""
async def mainMethod_():
    while True:
        #global session
        #async with aiohttp.ClientSession() as session:
            await getUserToken_()
            t1=time.perf_counter_ns()
            while True:
                #asyncio.run(getIntermediateOCR_())
                async with aiohttp.ClientSession() as session:
                    await getIntermediateOCR_(session)
                    time.sleep(5)
                    t2=time.perf_counter_ns()
                    dt=(t2-t1)
                await session.close()
                if(dt/((10**9)*3600)>=23):
                        break
            
async def mainProcess(session):
    if len(cabinetData)!=0:
        for data in cabinetData:
            recordId=str(data["recordId"])
            cabinetName=(data["cabinetName"])
            storageType=getStorageType_(cabinetName)
            fileNameList=data["images"]
            content=""
            dict={}
            textfile=open(os.path.join(UploadDir,recordId+"file.txt"),"w",encoding="utf-8")
            if len(fileNameList)!=0:
                for fname in fileNameList:
                    fileIsDownloaded=False
                    year=datetime.now().year
                    month=datetime.now().strftime("%B")
                    date_=datetime.now().day
                    fileName=str(fname)
                    flist=str(fileName).split(".")
                    fbaseName=flist[0]
                    fextension=flist[1]
                    if (storageType==3):
                        path=cabinetName.lower()+"-"+str(year)+"/"+str(month)+"/"+str(date_)+"/"+fileName
                        downloadfilefromHuawieCloud(path,fileName)
                        fileIsDownloaded=True
                    if storageType==5:
                        print("None")
                        getfilefromOnpremise(cabinetName,fileName)
                        #function to download file form onpremise
                    #implement_downloadFile(path,fileName)
                    if fileIsDownloaded==True:
                        downloadedFile=os.path.join(UploadDir,fileName)
                        text=process(downloadedFile,fextension)
                        os.remove(downloadedFile)
                        content=content+text
                if len(content)!=0:
                    textfile.write(content)
                    textfile.close()
                    dict["recordId"]=recordId
                    dict["ocrData"]=content
                    #implementsendResponse(dict)
                    await sendResponse_(dict)
                    #implementdeleteIntermediateOCR(recordId)
                    await deleteIntermediateOCR_(recordId)
                if len(content)==0:
                    print("Error in image processing")
        """
        for data in cabinetData:
            recordId=str(data["recordId"])
            cabinetName=(data["cabinetName"])
            fileNameList=data["images"]
            content=""
            dict={}
            textfile=open(os.path.join(UploadDir,recordId+"file.txt"),"w",encoding="utf-8")
            if len(fileNameList)!=0:
                for fname in fileNameList:
                    year=datetime.now().year
                    month=datetime.now().strftime("%B")
                    date_=datetime.now().day
                    fileName=str(fname)
                    path=cabinetName.lower()+"-"+str(year)+"/"+str(month)+"/"+str(date_)+"/"+fileName
                    flist=str(fileName).split(".")
                    fbaseName=flist[0]
                    fextension=flist[1]
                    if downloadfile(path,fileName):
                    #implement_downloadFile(path,fileName)
                        downloadedFile=os.path.join(UploadDir,fileName)
                        text=process(downloadedFile,fextension)
                        os.remove(downloadedFile)
                        content=content+text
                if len(content)!=0:
                    textfile.write(content)
                    textfile.close()
                    dict["recordId"]=recordId
                    dict["ocrData"]=content
                    #implementsendResponse(dict)
                    await sendResponse_(dict,session)
                    #implementdeleteIntermediateOCR(recordId)
                    await deleteIntermediateOCR_(recordId,session)
                if len(content)==0:
                    print("Error in image processing")
                """
#Only for testing purpose
def testtextextraction(fileName):
    path_=os.path.join(UploadDir,fileName)
    flist=str(fileName).split(".")
    fbaseName=flist[0]
    fextension=flist[1]
    text=process(path_,fextension)
    print(text)
async def deleteRecordsInIntermediateOCR():
    for data in cabinetData:
        recordId=data["recordId"]
        await deleteIntermediateOCR_(recordId)     

# async method definitinions   
"""
async def getUserToken():
    global userToken
    global header
    jsonUserAuth=json.dumps(userAuth)
    
    #response=requests.post(baseUrl+"/api/login",json=jsonUserAuth)
    response=await requests.post(baseUrl+"/api/login",json=jsonUserAuth)
    parseJson=json.loads(response.json())

    userToken=parseJson["token"]
    header={"Authorization":"Bearer "+userToken}
    response.close()
"""
async def getUserToken_():
    global userToken
    global header
    header={"Content-Type": "application/json"}
    jsonUserAuth=json.dumps(userAuth)
    content=jsonUserAuth.encode('utf-8')
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(baseUrl+"/api/auth/login",headers=header,data=jsonUserAuth) as response:
                
                if response.status<300:
                    pjson=await response.json()
                    userToken=pjson["user"]["token"]
                    print("took a userToken")
                    header["Authorization"]="Bearer "+userToken
                    
                else:
                    print("Bad response")
                    print(response.__str__())
                response.close()
        except:
            print("Error occured while getting userToken")
    await session.close()   
             
"""               
async def getIntermediateOCR():
    global cabinetData
    response=await requests.get(baseUrl+"/"+"api/manage-ocr/get-intermediate-ocr/"+OCRtype,headers=header)
    if response.status_code()<300:
        parsejson=json.loads(response.json())
        cabinetData=parsejson["IntermediateOcr"]
"""
async def getIntermediateOCR_(session):
    global cabinetData
    #async with aiohttp.ClientSession() as session:
    #try:
    async with session.get(baseUrl+"/api/manage-ocr/get-intermediate-ocr/"+OCRtype,headers=header) as response:
        if response.status<300:
            print("Listening..")
            parsejson=await response.json()
            cabinetData=parsejson["IntermediateOcr"]
            #print(cabinetData)
        else:
            print("Bad response")
            print(response.content.__str__())  
        response.close()
    await mainProcess(session)
    #except Exception(e):
        
        
        
#async def getfilepath(recordId,cabinetname,fileName):
    
def downloadfilefromHuawieCloud(filepath,fileName):
    global fileList
    #create s3 client with huawei cloud credentials
    accessKeyId=huaweiObjectStorageConfig["huaweiObsAccessKey"]
    secretAccessKey=huaweiObjectStorageConfig["huaweiObsSecreatAccessKey"]
    endPoint=huaweiObjectStorageConfig["huaweiObsServerEndpoint"]
    
    obsClient=ObsClient(
        access_key_id=accessKeyId,
        secret_access_key=secretAccessKey,
        server=endPoint
    )
    #print(accessKeyId+" # "+secretAccessKey+" # "+endPoint)
    
    bucketName=huaweiObjectStorageConfig["bucketName"]
    objectKey=filepath
    #objectKey="dev_huawei_zone_ocr-2023/March/1/63ff1c7c60feb53b941e0156_00001.png"
    dfilePath=os.path.join(UploadDir,fileName)
    try:
        response=obsClient.downloadFile(bucketName, objectKey,downloadFile=dfilePath)
        if response.status<300:
            print("Downloaded Successfully")
            obsClient.close()
            return True
        else:
            print(response.errorMessage)
            print(response.content.__str__())  
            obsClient.close()
            return False
        
    except:
        import traceback
        print(traceback.format_exc())
        print("Error occured while downloading the file")
        obsClient.close()
        return False
"""    
async def sendResponse(dict):
    jsonResponse=json.dumps(dict)
    url=apiConfig["enterpriseSearchHost"]+":"+apiConfig["enterpriseSearchPort"]
    response=await requests.put(url+"/"+"api/enterpriseSearch/add-ocr-data",json=jsonResponse,headers=header)
    if response.status_code()<300:
        print("Response has been sent Successfully")
    else:
        print("Error in sending response")
    response.close()
"""
def getfilefromOnpremise(cabinetName,fileName):
    filepath=r"C:\DOCUBINETLOCALFILES\\" + cabinetName + "\\" + fileName
    destinationpath=os.path.join(UploadDir,fileName)
    shutil.copy2(filepath, destinationpath)
       
async def sendResponse_(dict,session):
    jsonResponse=json.dumps(dict)
    url=apiConfig["enterpriseSearchHost"]+":"+apiConfig["enterpriseSearchPort"]
    #async with aiohttp.ClientSession() as session:
    try:
        async with session.put(url+"/api/enterprise-search/add-ocr-data",headers=header,data=jsonResponse) as response:
            if response.status<300:
                print("Extracted content has been sent Successfully")
            else:
                print("Bad response status")
                print(response.content.__str__())  
            response.close()
    except:
        print("Error occured while sending ExtractedText")
"""        
async def deleteItermediateOCR(recordId):
    response=await requests.delete(baseUrl+"/delete-intermediate-ocr/"+recordId,headers=header)
    if response.status_code<300:
        print("deleted IntermdiateOCRrecord successfully")       
    else:
        print("Error in deleting IntermdiateOCRrecord")
    response.close()
"""
async def deleteIntermediateOCR_(recordId,session):
    #async with aiohttp.ClientSession() as session:
    try:
        async with session.delete(baseUrl+"/api/manage-ocr/delete-intermediate-ocr/"+recordId,headers=header) as response:
            if response.status<300:
                print("deleted IntermdiateOCRrecord successfully")       
            else:
                print("Bad response status")
                print(response.content.__str__())  
            response.close()
    except:
        print("Error occured while deleting IntermediateOCRREcord")

def getStorageType_(cabinetName):
    client=MongoClient("mongodb+srv://sa:i5sjdrShyfoOowvY@cluster0.iqvet.mongodb.net/docubinet?retryWrites=true&w=majority")
    db = client['docubinet']
    collectionStorages = db['storages']
    collectionCabinet = db['cabinets']
    for cabinet in collectionCabinet.find():
            if cabinetName==cabinet['cabinetName']:
                return cabinet['location']['storageType']
  
asyncio.run(mainMethod_())