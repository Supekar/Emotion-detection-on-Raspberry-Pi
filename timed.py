import re
import schedule
import time
#from datetime import datetime
import argparse
import base64
import picamera
import json,ast
import string
import datetime
import requests


from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
API_ENDPOINT =""

def takephoto():
    camera = picamera.PiCamera()
    camera.capture('image.jpg')
    camera.close()
    
def detect_faces():
    takephoto() # First take a picture
    """Run a label request on a single image"""

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open('image.jpg', 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'FACE_DETECTION',
                    'maxResults': 10
                }]
            }]
        })
        response = service_request.execute()
    return response

def clean_data(raw_data):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(st)
    joyquotientsum=0
    angerquotientsum=0
    surprisequotientsum=0
    sorrowquotientsum=0
    d=raw_data
    o =0;
    result = {}
    reponses = d["responses"]
       
    for i in reponses:
        p = i.get("faceAnnotations")
        for j in p:
            o +=1
            #print(o)
            print(j.get("joyLikelihood"))
            joyfactor=j.get("joyLikelihood")
            angerfactor=j.get("angerLikelihood")
            surprisefactor=j.get("surpriseLikelihood")
            sorrowfactor=j.get("sorrowLikelihood")
            #print(joy,"joy")
            #print(j.get("angerLikelihood"),"anger")
            #print(j.get("sorrowLikelihood"),"sorrow")
            #print(j.get("surpriseLikelihood"),"surprise")
            if joyfactor == "VERY_UNLIKELY":
                joyquotient=0.2
            elif joyfactor == "UNLIKELY":
                joyquotient=0.4
            elif joyfactor == "POSSIBLE":
                joyquotient=0.6
            elif joyfactor == "LIKELY":
                joyquotient=0.8
            elif joyfactor == "VERY_LIKELY":
                joyquotient=1
            joyquotientsum+=joyquotient
            if sorrowfactor == "VERY_UNLIKELY":
                sorrowquotient=0.2
            elif sorrowfactor == "UNLIKELY":
                sorrowquotient=0.4
            elif sorrowfactor == "POSSIBLE":
                sorrowquotient=0.6
            elif sorrowfactor == "LIKELY":
                sorrowquotient=0.8
            elif sorrowfactor == "VERY_LIKELY":
                sorrowquotient=1
            sorrowquotientsum+=sorrowquotient
            if surprisefactor == "VERY_UNLIKELY":
                surprisequotient=0.2
            elif surprisefactor == "UNLIKELY":
                surprisequotient=0.4
            elif surprisefactor == "POSSIBLE":
                surprisequotient=0.6
            elif surprisefactor == "LIKELY":
                surprisequotient=0.8
            elif surprisefactor == "VERY_LIKELY":
                surprisequotient=1
            surprisequotientsum+=surprisequotient
            if angerfactor == "VERY_UNLIKELY":
                angerquotient=0.2
            elif angerfactor == "UNLIKELY":
                angerquotient=0.4
            elif angerfactor == "POSSIBLE":
                angerquotient=0.6
            elif angerfactor == "LIKELY":
                angerquotient=0.8
            elif angerfactor == "VERY_LIKELY":
                angerquotient=1
            angerquotientsum+=angerquotient
            #print(joyquotientsum)
            result[o] = [j["joyLikelihood"],j["angerLikelihood"],j["sorrowLikelihood"],j["surpriseLikelihood"]]
            #print(result[o])
            
       #print(result)   
    joyquotientsum=joyquotientsum/o
    angerquotientsum=angerquotientsum/o
    surprisequotientsum=surprisequotientsum/o
    sorrowquotientsum=sorrowquotientsum/o
    print(joyquotientsum)
    print(sorrowquotientsum)
    print(angerquotientsum)
    print(surprisequotientsum)
    nums = [joyquotientsum, sorrowquotientsum, surprisequotientsum, angerquotientsum]
    nums.sort(reverse=True)

    print("after sorting list")
    print(nums[0])
    if sorrowquotientsum == nums[0]:
        finalemotion='sorrow'
        finalnumber=sorrowquotientsum
    elif angerquotientsum == nums[0]:
        finalemotion='anger'
        finalnumber=angerquotientsum
    elif surprisequotientsum == nums[0]:
        finalemotion='surprise'
        finalnumber=surprisequotientsum
    elif joyquotientsum == nums[0]:
        finalemotion='joy'
        finalnumber=joyquotientsum
    with open('packet.json') as json_data:
        d1 = json.load(json_data)
        d1['timestamp']=st
        x=d1['faces']
        


    for i in x:
        
        i['emotion']= finalemotion
        i['degree']=finalnumber
        i['count']=o
    print(d1)
    return d1

def send_data(data):
    #requests.post(url=API_ENDPOINT, data=data)
    print("done")


    
    
    

def job():
    print("hi")
    
    raw_data = detect_faces()
    data = clean_data(raw_data)
    send_data(data)
    


#schedule.every(10).minutes.do(job)
#schedule.every().hour.do(job)
#schedule.every().day.at("22:17").do(job)
schedule.every(5).seconds.do(job)


if __name__ == '__main__':

    job()

while 1:
    schedule.run_pending()
    time.sleep(1)