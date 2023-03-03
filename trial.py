
import threading
import sched
import schedule
import time
import requests_async as requests_
import requests
import aiohttp
import asyncio
from datetime import datetime
from pymongo import MongoClient
import os


"""
schedule=sched.scheduler(time.time,time.sleep)
schedule.enter(5,1,b)
schedule.enter(1,1,a)
count=0
while count<10:
    schedule.run()
    count=count+1
"""
async def a():
    await a_()
async def a_():
    print("1")    
async def b():
    print("5")

def fn():
    schedule.every(5).seconds.do(asyncio.run,a())
    #schedule.every(5).seconds.do(b_())
    
    count=1
    while True:
        
        schedule.run_pending()
        
        count=count+1

def countTime():
    t1=time.perf_counter_ns()
    for i in range(5):
        print("#")
    t2=time.perf_counter_ns()
    dt=(t2-t1)/((10**9)*3600*12)
    print(dt)
"""
while True:
    asyncio.run(b())
    t1=time.perf_counter_ns()
    while True:
        asyncio.run(a_())
        time.sleep(5)
        t2=time.perf_counter_ns()
        dt=(t2-t1)
        if(dt/((10**9))>=10):
            break
"""
"""
now=datetime.now()
month=now.strftime("%B")
print(month)
"""
"""
def getStorageType():
    client=MongoClient("mongodb+srv://sa:i5sjdrShyfoOowvY@cluster0.iqvet.mongodb.net/docubinet?retryWrites=true&w=majority")
    db = client['docubinet']
    collectionStorages = db['storages']
    collectionCabinet = db['cabinets']
    collectionIntermediateOCR = db['intmed-ocrs']
    for doc in collectionIntermediateOCR.find():
        doc["cabinetName"]
        for cabinet in collectionCabinet.find():
            if doc['cabinetName']==cabinet['cabinetName']:
                return cabinet['location']['storageType']
"""
"""
def getStorageType_(cabinetName):
    client=MongoClient("mongodb+srv://sa:i5sjdrShyfoOowvY@cluster0.iqvet.mongodb.net/docubinet?retryWrites=true&w=majority")
    db = client['docubinet']
    collectionStorages = db['storages']
    collectionCabinet = db['cabinets']
    for cabinet in collectionCabinet.find():
            if cabinetName==cabinet['cabinetName']:
                return cabinet['location']['storageType']
print(getStorageType_("DEV_HUAWEI_ZONE_OCR"))
"""
import shutil
path=os.getcwd()
folder_1=os.path.join(path,"folder_1")
src_file = r"F:\DMS\Docubinet_FulltextOCR\MicrosoftTeams-image (2).png"
dst_file = os.path.join(folder_1,"f.png")

shutil.copy2(src_file, dst_file)

