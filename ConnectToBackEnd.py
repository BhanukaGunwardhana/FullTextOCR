import requests
import json
from datetime import datetime
import os
from obs import ObsClient
from CharacterExtraction import *

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

userToken=""
baseUrl=apiConfig["userPortalHost"]+":"+"userPortalPort"
OCRtype="2"
fileList=[]

path=os.getcwd()
UploadDir=os.path.join(path,"UploadDir")
if not os.path.isdir(UploadDir):
    os.mkdir(UploadDir)

#Creating directory for save extracted textfile
OCRDir=os.path.join(path,"OCRDir")
if not os.path.isdir(OCRDir):
    os.mkdir(OCRDir)



def mainProcess():
    getUserToken()
    getIntermeadiateOCR()
    if len(cabinetData)!=0:
        dic2={}
        for data in cabinetData:
            recordId=str(data["recordId"])
            cabinetName=str(data["cabinetname"])
            fileNameList=data["images"]
            dic1={}
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
                dic1[fileName]=text
            dic2[cabinetName]=dic1
            
            
           
                
            
            



def getUserToken():
    global userToken
    jsonUserAuth=json.dump(userAuth)
    
    response=requests.post(baseUrl+"/api/login",json=jsonUserAuth)
    parseJson=json.loads(response.json())

    userToken=parseJson["token"]
    response.close()

def getIntermeadiateOCR():
    global cabinetData
    header={"Authorization":"Bearer {userToken}"}
    response=requests.get(baseUrl+"/"+"api/manage-ocr/get-intermediate-ocr/{OCRtype}",headers=header)
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
        res=obsClient.getObject(bucketName, objectKey, downloadPath=dfilePath)
        if res.status()<300:
            print("Downloadede Successfully")
            fileList.append(fileName)
        else:
            print(res.errorMessage)
    except:
        import traceback
        print(traceback.format_exc())
    
    
