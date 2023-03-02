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



userAuth={'username':'superuser','password':'superuser3dms'}
apiConfig={ "userPortalHost": "http://localhost",# "https://www.docubinet.com"
  "userPortalPort": "5000",
  "enterpriseSearchHost": "http://localhost",#//www.docubinet.com
  "enterpriseSearchPort": "5003"}
huaweiObjectStorageConfig={ 
  "huaweiObsAccessKey": "LZZDXMVWWA8ZTECX26RB",#LZZDXMVWWA8ZTECX26RB
  "huaweiObsSecreatAccessKey": "8xJElsflfLe0ut2coPsPYlqXEdFbJsR6qoroJmio",
  "huaweiObsServerEndpoint": "https://obs.ap-southeast-3.myhuaweicloud.com",
  "bucketName": "001-docubinet",
}
"""
OBS_ACCESS_KEY_ID=LZZDXMVWWA8ZTECX26RB
OBS_SECRET_ACCESS_KEY=8xJElsflfLe0ut2coPsPYlqXEdFbJsR6qoroJmio
OBS_SERVER_ENDPOINT=obs.ap-southeast-3.myhuaweicloud.com
OBS_LOCATION=ap-southeast-3
OBS_BUCKET_NAME=001-docubinet 
"""
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
def mainMethod_():
    while True:
        asyncio.run(getUserToken_())
        print("took a userToken")
        t1=time.perf_counter_ns()
        while True:
            asyncio.run(getIntermediateOCR_())
            time.sleep(5)
            t2=time.perf_counter_ns()
            dt=(t2-t1)
            if(dt/((10**9)*3600)>=23):
                break
async def mainProcess():
    if len(cabinetData)!=0:
        for data in cabinetData:
            recordId=str(data["recordId"])
            cabinetName=(data["cabinetName"])
            fileNameList=data["images"]
            content="Hi"
            dict={}
            textfile=open(os.path.join(UploadDir,recordId+"file.txt"),"w",encoding="utf-8")
        
            for fname in fileNameList:
                year=datetime.now().year
                month=datetime.now().strftime("%B")
                date_=datetime.now().day
                fileName=str(fname)
                path=cabinetName.lower()+"-"+str(year)+"/"+str(month)+"/"+str(date_)+"/"+fileName
                flist=str(fileName).split(".")
                fbaseName=flist[0]
                fextension=flist[1]
                downloadfile(path,fileName)
                #implement_downloadFile(path,fileName)
                downloadedFile=os.path.join(UploadDir,fileName)
                text=process(downloadedFile,fextension)
                os.remove(downloadedFile)
                content=content+text
            
            textfile.write(content)
            textfile.close()
            dict["recordId"]=recordId
            dict["ocrData"]=content
            #implementsendResponse(dict)
            await sendResponse_(dict)
            #implementdeleteIntermediateOCR(recordId)
            await deleteIntermediateOCR_(recordId)
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
#syncronization of methods with main thread
"""
def implement_getUserToken():
    thread=threading.Thread(target=getUserToken)
    thread.start()
    thread.join()
def implement_getIntermediateOCR():
    thread=threading.Thread(target=getIntermediateOCR)
    thread.start()
    thread.join()
    mainProcess()
def implement_downloadFile(filepath,fileName):
    thread=threading.Thread(target=downloadfile,args=(filepath,fileName))
    thread.start()
    thread.join()
def implementsendResponse(dict):
    thread=threading.Thread(target=sendResponse,args=(dict,))
    thread.start()
    thread.join()    
def implementdeleteIntermediateOCR(recordId):
    thread=threading.Thread(target=deleteItermediateOCR,args=(recordId,))
    thread.start()
    thread.join()
"""
#method definitinions   
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
    global session
    header={"Content-Type": "application/json"}
    jsonUserAuth=json.dumps(userAuth)
    content=jsonUserAuth.encode('utf-8')
    async with aiohttp.ClientSession() as session:
        async with session.post(baseUrl+"/api/auth/login",headers=header,data=jsonUserAuth) as response:
            
            if response.status<300:
                #print(response.__str__())
                pjson=await response.json()
                userToken=pjson["user"]["token"]
                #header={"Authorization":"Bearer "+userToken}
                header["Authorization"]="Bearer "+userToken
            else:
                print(response.__str__())
                print("not ok")
            
"""               
async def getIntermediateOCR():
    global cabinetData
    response=await requests.get(baseUrl+"/"+"api/manage-ocr/get-intermediate-ocr/"+OCRtype,headers=header)
    if response.status_code()<300:
        parsejson=json.loads(response.json())
        cabinetData=parsejson["IntermediateOcr"]
"""
async def getIntermediateOCR_():
    global cabinetData
    async with aiohttp.ClientSession() as session:
        async with session.get(baseUrl+"/api/manage-ocr/get-intermediate-ocr/"+OCRtype,headers=header) as response:
            if response.status<300:
                print("ok")
                parsejson=await response.json()
                cabinetData=parsejson["IntermediateOcr"]
                print(cabinetData)
            else:
                print(response.content.__str__())  
            response.close()
    await mainProcess()
#async def getfilepath(recordId,cabinetname,fileName):
    
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
    print(accessKeyId+" # "+secretAccessKey+" # "+endPoint)
    
    bucketName=huaweiObjectStorageConfig["bucketName"]
    objectKey=filepath
    #dev_huawei_zone_ocr-2023/63ff1c7c60feb53b941e0156_00001.png
    #objectKey="dev_huawei_zone_ocr-2023/March/1/63ff1c7c60feb53b941e0156_00001.png"
    dfilePath=os.path.join(UploadDir,fileName)
    try:
       # response=obsClient.getObject(bucketName, objectKey, downloadPath=os.path.join(UploadDir,fileName),#downloadPath=dfilePath
        #                             loadStreamInMemory=True)
        response=obsClient.downloadFile(bucketName, objectKey,downloadFile=os.path.join(UploadDir,fileName),#downloadPath=dfilePath
        
                                     )
        if response.status<300:
            #with open(dfilePath,"wb") as f:
             #   shutil.copyfileobj(response., f)
            
            print("Downloaded Successfully")
            
            fileList.append(fileName)
        else:
            print(response.errorMessage)
            print(response.status)
        
    except:
        import traceback
        print(traceback.format_exc())
        print("Except block was called")
    obsClient.close()
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
async def sendResponse_(dict):
    jsonResponse=json.dumps(dict)
    url=apiConfig["enterpriseSearchHost"]+":"+apiConfig["enterpriseSearchPort"]
    async with aiohttp.ClientSession() as session:
        async with session.put(url+"/api/enterprise-search/add-ocr-data",headers=header,data=jsonResponse) as response:
            if response.status<300:
                print("Response has been sent Successfully")
            else:
                print(response.status)
                print("Error in sending response")
            response.close()
"""        
async def deleteItermediateOCR(recordId):
    response=await requests.delete(baseUrl+"/delete-intermediate-ocr/"+recordId,headers=header)
    if response.status_code<300:
        print("deleted IntermdiateOCRrecord successfully")       
    else:
        print("Error in deleting IntermdiateOCRrecord")
    response.close()
"""
async def deleteIntermediateOCR_(recordId):
    async with aiohttp.ClientSession() as session:
        async with session.delete(baseUrl+"/api/manage-ocr/delete-intermediate-ocr/"+recordId,headers=header) as response:
            if response.status<300:
                print("deleted IntermdiateOCRrecord successfully")       
            else:
                print("Error in deleting IntermdiateOCRrecord")
            response.close()
mainMethod_()