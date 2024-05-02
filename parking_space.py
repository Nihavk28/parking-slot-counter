import cv2
import pickle


# image=cv2.imread('parking_lot_image.jpg')

w=108
h=48

try:
    with open('parknpos','rb') as f:
        positionlist=pickle.load(f)
    
except:
    positionlist=[]

def mouseclick(events,x,y,flags,params):
    if events==cv2.EVENT_LBUTTONDOWN:
        positionlist.append((x,y))
    if events==cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(positionlist):
            x1 , y1= pos
            if x1<x<x1+w and y1<y<y1+h:
                positionlist.pop(i)
    with open('parknpos','wb') as f:
        pickle.dump(positionlist,f)
        

while True:
   
    img=cv2.imread('parking_lot_image.png')
    
    for pos in positionlist:
        cv2.rectangle(img,(pos[0] ,pos[1]),(pos[0] + w, pos[1]+ h), (200,105,200),2)
    


    cv2.imshow('Image', img)
    cv2.setMouseCallback("Image",mouseclick)
    
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break