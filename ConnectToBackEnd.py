#import requests
import requests_async as requests
import json
from datetime import datetime
import os
from obs import ObsClient
from CharacterExtraction import *
import threading
import schedule
import flask

userAuth={"userName" :"superuser", "passWord":"superuser3dms"}
apiConfig={ "userPortalHost": "https://www.docubinet.com",
  "userPortalPort": 5000,
  "enterpriseSearchHost": "https://www.docubinet.com",
  "enterpriseSearchPort": 5003,}
huaweiObjectStorageConfig={ 
  "huaweiObsAccessKey": "LZZDXMVWWA8ZTECX26RB",
  "huaweiObsSecreatAccessKey": "8xJElsflfLe0ut2coPsPYlqXEdFbJsR6qoroJmio",
  "huaweiObsServerEndpoint": "obs.ap-southeast-3.myhuaweicloud.com",
  "bucketName": "001-docubinet",
}

baseUrl=apiConfig["userPortalHost"]+":"+apiConfig["userPortalPort"]
OCRtype="2"
fileList=[]

path=os.getcwd()
UploadDir=os.path.join(path,"UploadDir")
if not os.path.isdir(UploadDir):
    os.mkdir(UploadDir)
    
def mainMethod():
    schedule.every(24).hours.do(implement_getUserToken)
    schedule.every(5).seconds.do(implement_getIntermediateOCR())
    while True:
        schedule.run_pending()
def mainProcess():
    #getUserToken will run fisrt and main thread will stay until thread1 finished
    #thread1=threading.Thread(target=getUserToken)
    #thread1.start()
    #thread1.join()
    #After completion of thread1 thread2 wil start and also main thread will stay until completion of thread2
    #thread2=threading.Thread(target=getIntermediateOCR)
    #thread1.start()
    #thread2.join()
    #getUserToken()
    #getIntermeadiateOCR()
    if len(cabinetData)!=0:
        dict2={}
        for data in cabinetData:
            recordId=str(data["recordId"])
            cabinetName=str(data["cabinetname"])
            fileNameList=data["images"]
            content=""
            for fname in fileNameList:
                fileName=str(fname)
                path=cabinetName.lower()+"-"+datetime.now().year+"/"+fileName
                flist=str(fileName).split(".")
                fbaseName=flist[0]
                fextension=flist[1]
                downloadfile(path,fileName)
                downloadedFile=os.path.join(UploadDir,fileName)
                text=process(downloadedFile,fextension)
                os.remove(downloadedFile)
                content=content+text
            dict2[recordId]=content
            deleteItermediateOCR(recordId)
        sendResponse(dict2)  
#getUserToken will run fisrt and main thread will stay until thread1 finished            
def implement_getUserToken():
    thread1=threading.Thread(target=getUserToken)
    thread1.start()
    thread1.join()

#After completion of thread1 thread2 wil start and also main thread will stay until completion of thread2
def implement_getIntermediateOCR():
    thread2=threading.Thread(target=getIntermediateOCR)
    thread2.start()
    thread2.join()
    mainProcess()
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

async def getIntermediateOCR():
    global cabinetData
    response=await requests.get(baseUrl+"/"+"api/manage-ocr/get-intermediate-ocr/"+OCRtype,headers=header)
    parsejson=json.loads(response.json())
    cabinetData=parsejson["IntermediateOcr"]


def downloadfile(filepath,fileName):
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
    bucketName=huaweiObjectStorageConfig["bucketName"]
    objectKey=filepath
    dfilePath=os.path.join(UploadDir,fileName)
    try:
        response=obsClient.getObject(bucketName, objectKey, downloadPath=dfilePath)
        if response.status()<300:
            print("Downloaded Successfully")
            fileList.append(fileName)
        else:
            print(response.errorMessage)
        
    except:
        import traceback
        print(traceback.format_exc())
    obsClient.close()
    
async def sendResponse(dic2):
    jsonResponse=json.dumps(dic2)
    url=apiConfig["enterpriseSearchHost"]+":"+apiConfig["enterpriseSearchPort"]
    response=await requests.put(url+"/"+"api/enterpriseSearch/add-ocr-data",json=jsonResponse,headers=header)
    if response.status_code()<300:
        print("Response has been sent Successfully")
    else:
        print("Error in sending response")
    response.close()

async def deleteItermediateOCR(recordId):
    response=await requests.delete(baseUrl+"/delete-intermediate-ocr/"+recordId,headers=header)
    if response.status_code<300:
        print("deleted IntermdiateOCRrecord successfully")       
    else:
        print("Error in deleting IntermdiateOCRrecord")
    response.close()

mainMethod()