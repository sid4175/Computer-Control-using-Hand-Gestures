import cv2 
import numpy as np
import pyautogui
cap=cv2.VideoCapture(0)

bgCap=0
z=0
p=0
ay=0
apy=1
ply=[0]
plx=[0]
k=0
r1=0
l1=0
d11=0
u1=0
htol=9
def removeBG(hsv):
    fgmask=bgM.apply(hsv,learningRate=0)
    kern=np.ones((9,9),np.uint8)
    fgmask = cv2.erode(fgmask, kern, iterations=1)
    res = cv2.bitwise_and(hsv, hsv, mask=fgmask)
    return res

    
while(1):        
    _, frame = cap.read()
    frame=cv2.flip(frame,1)
    cv2.rectangle(frame,(400,400),(800,100),(0,255,0),0)
    frame=frame[200:400,400:800]
    panfree=np.copy(frame)
    #Bgr to Hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('main frame', frame)
    
    #d1 = np.zeros(frame.shape, np.uint8)
    if bgCap==1:
        img=removeBG(hsv)
        cv2.imshow('fg_mask', img)
        #zooming operation
        if z==1:
            hi,si,vi=cv2.split(img)
            _, th1 = cv2.threshold(vi,40, 255, cv2.THRESH_BINARY)
            cv2.imshow("thr10",th1)
            _, cs, hierarchy= cv2.findContours(th1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            d1 = np.zeros(img.shape, np.uint8)
            m_area=-1
            for i in range(len(cs)):
                ct=cs[i]
                ar = cv2.contourArea(ct)
                
                if ar>7000:
                    pyautogui.keyDown('ctrl')
                    print("zoom in")
                    #pyautogui.scroll(10) 
                    pyautogui.press('+')
                elif ar>800:
                    pyautogui.keyDown('ctrl')
                    #pyautogui.scroll(-10) 
                    print("zoom out")
                    pyautogui.press('-')

                ct=cs[i]
                hul = cv2.convexHull(ct)
                cv2.drawContours(d1, [ct], 0, (0, 255, 0), 2)
                cv2.drawContours(d1, [hul], 0, (0, 0, 255), 2)
            cv2.imshow('output', d1)
            pyautogui.keyUp('ctrl')        
            
        #color range for cursor
        """lower_blue = np.array([100,90,100]) 
        upper_blue = np.array([245,255,255])"""
        #color range for cursor 
        lower_blue = np.array([100,100,85]) 
        upper_blue = np.array([210,255,255])    
        #track blue cursor   
        mask = cv2.inRange(img, lower_blue, upper_blue) 
        res = cv2.bitwise_and(frame,frame, mask= mask)
        cv2.imshow('mask',mask) 
        cv2.imshow('res',res)
        _, thresh1 = cv2.threshold(mask,90, 255, cv2.THRESH_BINARY)
        _, contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        max_area_blue=-1
        area=0
        for i in range(len(contours)):
            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if(area>max_area_blue):
                #print("blue area",area)
                max_area_blue=area
                ci=i
                cnt=contours[ci]
        if area>5:
            a,b,w,h = cv2.boundingRect(cnt)
            axb,byb,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(a,b),(a+w,b+h),(0,0,255),2)
            #print(a,b)
            if a!=0 and b!=0:
                ox=240
                nx=1366
                a=a*nx/ox
                oy=198
                ny=768
                b=b*ny/oy
                pyautogui.moveTo(a,b)
                
        #double click        
        if area>10 and p==0 and z==0:
            l_ylw = np.array([18,100,80])
            u_ylw = np.array([52,255,255])
            mask_click=cv2.inRange(img,l_ylw,u_ylw)
            res_click=cv2.bitwise_and(frame,frame,mask=mask_click)
            _, thr_click = cv2.threshold(mask_click,100, 255, cv2.THRESH_BINARY)
            _, cnt_click, hierarchy = cv2.findContours(thr_click,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            max_area_click=-1
            area_click=0
            for i in range(len(cnt_click)):
                cc=cnt_click[i]
                area_click = cv2.contourArea(cc)
                if(area_click>max_area_click):
                #print("yellow area",area)
                    max_area_click=area_click
                    cc=cnt_click[i]
                cay,cby,cwy,chy = cv2.boundingRect(cc)           
            if area_click>7:
                #print(axb,cay,byb,cby)
                if axb-cay<100 and byb-cby<100:
                    print("click")
                    pyautogui.doubleClick()
        if p==1:    #panning 
            z=0
            """l_ylw = np.array([2,15,90])
            u_ylw = np.array([25,255,255])"""
            l_ylw = np.array([18,90,100])
            u_ylw = np.array([52,255,255])
            mask_pan=cv2.inRange(img,l_ylw,u_ylw) 
            res_pan=cv2.bitwise_and(frame,frame,mask=mask_pan)
            cv2.imshow('pan_mask',mask_pan) 
            cv2.imshow('pan_res',res_pan)
            _, thr_pan = cv2.threshold(mask_pan,110, 255, cv2.THRESH_BINARY)
            _, cnt_pan, hierarchy = cv2.findContours(thr_pan,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            max_area_ylw=-1
            area_ylw=0
            i=0
            tx1=0
            tx2=0
            for i in range(len(cnt_pan)):
                cp=cnt_pan[i]
                area_ylw = cv2.contourArea(cp)
                if(area_ylw>max_area_ylw):
                #print("yellow area",area)
                    max_area_ylw=area_ylw
                    cy=i
                    cp=cnt_pan[cy]
                if ay!=0:
                    apy=ay
                    
            if area_ylw>15:
                cp=cnt_pan[i]
                ay,by,wy,hy = cv2.boundingRect(cp)
                
                cv2.rectangle(panfree,(ay,by),(ay+wy,by+hy),(255,0,0),0)
                if ay!=0 and by!=0:
                    ox=242
                    nx=1000
                    ay=ay*nx/ox
                    oy=198
                    ny=1000
                    by=by*ny/oy
                    plx.append(ay)
                    ply.append(by)
                    #print(ay,by)
    
                len1=len(ply)-1
                if len1>5:
                    for j in range(len1-4,len1):
                        tx1=0
                        tx2=0
                        if(ply[j+1]<=ply[j]+htol or ply[j+1]>ply[j]-htol):
                            for i in range(1,len(plx)-1):
                                #print("l1",plx[i],plx[i+1],ply[j])
                                if(plx[i+1]>plx[i]) and tx1<5:
                                    tx1=tx1+1
                                #else: tx1=0   
                                #print("l2",plx[i],plx[i+1],ply[j])
                                elif(plx[i+1]<plx[i]):
                                    tx1=tx1-1
                                else: tx1=0    
                                
                                      
                        if(plx[j+1]<=plx[j]+htol or plx[j+1]>plx[j]-htol):
                            for i in range(1,len(ply)-1):
                                #print("l1",plx[i],plx[i+1],ply[j])
                                if(ply[i+1]>ply[i] and tx2<5):
                                    tx2=tx2+1
                                #else: tx1=0   
                                #print("l2",plx[i],plx[i+1],ply[j])
                                elif(ply[i+1]<ply[i]):
                                    tx2=tx2-1
                                else: tx2=0    
                                
                                    
                               
                if tx1>0 and tx1>tx2:
                    print('right')
                    r1=r1+1
                    pyautogui.press("right")
                elif tx1<0 and tx1<tx2:
                    print('left')
                    l1=l1+1
                    pyautogui.press("left")
                elif tx2>0 and tx2>tx1:
                    print('down')
                    d11=d11+1
                    pyautogui.click()
                    pyautogui.scroll(20)
                elif tx2<0 and tx2<tx1:
                    print('up')
                    u1=u1+1
                    pyautogui.click()
                    pyautogui.scroll(-20)  
                """if tx1!=0 and tx2!=0:
                    print(tx1,tx2)
                    tx1=0
                    tx2=0"""
               
            cv2.imshow('framepan',panfree) 
                
        cv2.imshow('framenew',frame) 
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    if cv2.waitKey(1) & 0xFF==ord('b'):
        bgM = cv2.createBackgroundSubtractorMOG2(0,82)
        bgCap= 1
    if cv2.waitKey(1)& 0xFF==ord('z'):
        z=1
    if cv2.waitKey(1)& 0xFF==ord('x'):
        z=0
        p=0
    if cv2.waitKey(1)& 0xFF==ord('p'):
        p=1

cv2.destroyAllWindows() 
cap.release()
            
            
