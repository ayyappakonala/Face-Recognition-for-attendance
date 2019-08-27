import cv2
import numpy as np
import sqlite3
from datetime import datetime

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)
recog=cv2.face.LBPHFaceRecognizer_create()
recog.read("recog/trainingddata.yml")
id=0
font = cv2.FONT_HERSHEY_SIMPLEX
p={}
while True:
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        id,conf=recog.predict(gray[y:y+h,x:x+w])
        # print(id)
        if conf<60:
            cv2.putText(frame,str(id),(x,y+h),font,2,(255,255,255),2,cv2.LINE_AA)
            if str(id) in p:
            	p[str(id)]+=1
            else:
            	p[str(id)]=1
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) == ord('q'):
        break

conn=sqlite3.connect("C:/Users/ayyappa/Desktop/mp/student.sqlite3")
c=conn.cursor()
r=c.execute("select * from login_attend")
r=[]
for i,v in p.items():
	if v>=20:
		r.append(i)
n=[]
for i in r:
	k=c.execute("select name from login_users where rollno=?",(i,))
	for j in k:
		n.append(j[0])
for i in range(len(r)):
	c.execute("insert into login_attend(date,attendance,rollno,name) values(?,?,?,?)",(datetime.now().date(),"P",r[i],n[i],))
if r==[]:
	print("NOT REGISTERED!!!")	
conn.commit()
video_capture.release()
cv2.destroyAllWindows()