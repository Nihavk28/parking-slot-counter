import cv2
import numpy as np
import pickle



cap=cv2.VideoCapture('parking_lot_video.mp4')

#load the saved position file
with open('parknpos','rb') as f:
    postionlist=pickle.load(f)
    
w=108
h=48

def availableparkingspace(preprocessed_frame):
    counter =0
    if len(postionlist)!=0:
        for pos in postionlist:
            x,y=pos
            cropped_frame=preprocessed_frame[y:y+h , x:x+w]
            # cv2.imshow(str(x * y), cropped_frame)     
            count=cv2.countNonZero(cropped_frame)
            if count<1190:
                counter+=1
                color=(100,255,100)
            else:
                color=(100,100,255)
                
                
            cv2.rectangle(frame,(pos[0],pos[1]),(pos[0]+w,pos[1]+h),color,2) 
        
            cv2.putText(frame,str(count),(pos[0], pos[1]+5),0,0.5,[255,255,255],thickness=1,lineType=cv2.LINE_AA)
    
        cv2.rectangle(frame,(50,16),(50+w+170,16+h+15),(255,100,110),cv2.FILLED)
        cv2.putText(frame,f'Free Space:{counter}/{len(postionlist)}',(52,16+h),0,1,[255,255,255],thickness=2,lineType=cv2.LINE_AA)


while True:
    # To make the video play continuously
    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    ret,frame=cap.read()


    if ret:
        
        img_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
        # add guassian blur
        blur_img=cv2.GaussianBlur(img_gray,(3,3),1)
        
        # apply threshold on each of the frame of the video
        frame_threshold=cv2.adaptiveThreshold(blur_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,10)
         
        # to remove the noise ,apply  median blur
        median_blur=cv2.medianBlur(frame_threshold,5)
        
        #applying dilation to increase the thickness of edges
        kernal=np.ones((3,3),np.uint8)
        frame_dilate= cv2.dilate(median_blur,kernal, iterations=1)
        
        availableparkingspace(frame_dilate)
    
        cv2.imshow("video",frame)
        if cv2.waitKey(10) & 0XFF==ord('q'):
          break
    else:
        break
   
    