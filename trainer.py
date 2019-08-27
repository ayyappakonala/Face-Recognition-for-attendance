import cv2
import os
import numpy as np
from PIL import Image

recog=cv2.face.LBPHFaceRecognizer_create()
path="dataset/"

def getImagesWithID(path):
    ip=[os.path.join(path,f) for f in os.listdir(path)]
    f=[]
    ids=[]
    for i in ip:
        fi=Image.open(i).convert('L')
        fnp=np.array(fi,'uint8')
        # print(os.path.split(i)[-1].split("."))
        ids.append(int(os.path.split(i)[-1].split(".")[1]))
        f.append(fnp)
        # cv2.imshow("training",fnp)
        cv2.waitKey(10)
    return ids,f

ids,f=getImagesWithID(path)
recog.train(f,np.array(ids))
recog.save("recog/trainingddata.yml")
cv2.destroyAllWindows()
