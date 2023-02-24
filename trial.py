import threading
import sched
import schedule
import time

def a():
    print("1")
def b():
    print("5")
"""
schedule=sched.scheduler(time.time,time.sleep)
schedule.enter(5,1,b)
schedule.enter(1,1,a)
count=0
while count<10:
    schedule.run()
    count=count+1
"""
schedule.every(1).seconds.do(a)
schedule.every(5).seconds.do(b)

count=1
while count<10:
    schedule.run_pending()
    #count=count+1