import cv2
import numpy as np
cap= cv2.VideoCapture(0)
cap.set(10,200)
bgCap=0
def removeBG(hsv):
    fgmask=bgM.apply(hsv,learningRate=0)
    kern=np.ones((5,5),np.uint8)
    fgmask = cv2.erode(fgmask, kern, iterations=1)
    res = cv2.bitwise_and(hsv, hsv, mask=fgmask)
    return res
def n1(h):
    print("val changed:",h)
    return

cv2.namedWindow('lowerbar')
cv2.createTrackbar('h1', 'lowerbar', 0, 255, n1)
cv2.createTrackbar('s1', 'lowerbar', 0, 255, n1)
cv2.createTrackbar('v1', 'lowerbar', 0, 255, n1)

cv2.namedWindow('trackbar')
cv2.createTrackbar('h2', 'trackbar', 0, 255, n1)
cv2.createTrackbar('s2', 'trackbar', 0, 255, n1)
cv2.createTrackbar('v2', 'trackbar', 0, 255, n1)

while(1):
    _, frame = cap.read()
    frame=cv2.flip(frame,1)
    cv2.rectangle(frame,(400,400),(800,100),(0,255,0),0)
    frame=frame[200:400,400:800]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hue1 = cv2.getTrackbarPos('h1', 'lowerbar')
    sat1 = cv2.getTrackbarPos('s1', 'lowerbar')
    val1 = cv2.getTrackbarPos('v1', 'lowerbar')
    hue2 = cv2.getTrackbarPos('h2', 'trackbar')
    sat2 = cv2.getTrackbarPos('s2', 'trackbar')
    val2 = cv2.getTrackbarPos('v2', 'trackbar')
    if bgCap==1:
        img=removeBG(hsv)
        cv2.imshow('fg_mask', img)
        
        lower_blue = np.array([hue1,sat1,val1]) 
        upper_blue = np.array([hue2,sat2,val2])
        mask = cv2.inRange(img, lower_blue, upper_blue) 
        res = cv2.bitwise_and(frame,frame, mask= mask)
        cv2.imshow('mask',mask) 
        cv2.imshow('res',res)
        _, thresh1 = cv2.threshold(mask,70, 255, cv2.THRESH_BINARY)
        _, contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        d1 = np.zeros(img.shape, np.uint8)
        M_area=-1
        area=0
        for i in range(len(contours)):
            c=contours[i]
            area=cv2.contourArea(c)
            if area>M_area:
                M_area=area
                c=i
                cnt=contours[c]
        if area>10:
            a,b,w,h=cv2.boundingRect(cnt)
            cv2.rectangle(frame,(a,b),(a+w,b+h),(255,255,0),0)
            
    cv2.imshow('framenew',frame) 
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    if cv2.waitKey(1) & 0xFF==ord('b'):
        bgM = cv2.createBackgroundSubtractorMOG2(0,80)
        bgCap= 1
