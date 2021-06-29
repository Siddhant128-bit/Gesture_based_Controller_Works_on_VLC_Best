import cv2
import mediapipe as mp
import time
import math
import pyautogui
import screen_brightness_control as sbc
def main():
    cap=cv2.VideoCapture(0)

    mpHands=mp.solutions.hands
    mpDraw=mp.solutions.drawing_utils
    hands=mpHands.Hands()
    pTime=0
    cTime=0
    t_d=0
    t_cy=0
    t_cx=0
    activate_lock=0

    while True:
        ret,frame=cap.read()
        imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=hands.process(imgRGB)
        w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id,lm in enumerate(handLms.landmark):
                    h,w,c = frame.shape
                    cx,cy=int(lm.x*w),int(lm.y*h)
                    if (cx in range(int(w/8-65),int(w/8+65))) and (cy in range(int(h/2-80),int(h/2+80))) and activate_lock==0:
                        cv2.rectangle(frame,(int(w/8-65),int(h/2-80)),(int(w/8+65),int(h/2+80)),(255,0,0),5)
                        cv2.putText(frame,'Manipulate Sound',(40,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
                        pyautogui.PAUSE=0.005
                        if  id==8:
                            index_x=cx
                            index_y=cy
                            cv2.circle(frame,(cx,cy),5,(255,255,255),cv2.FILLED)
                        elif id ==4:
                            thumb_x=cx
                            thumb_y=cy
                            cv2.circle(frame,(cx,cy),5,(255,255,255),cv2.FILLED)
                        try:
                            distance=math.sqrt((index_x-thumb_x)**2+(index_y-thumb_y)**2)
                            if distance>t_d:
                                pyautogui.press('volumeup')
                                pyautogui.press('volumeup')
                            elif distance<t_d:
                                pyautogui.press('volumedown')
                                pyautogui.press('volumedown')

                            t_d=distance
                        except:
                            print('one of the other is mising')

                    elif (cx in range(int(7*w/8-60),int(7*w/8+60))) and (cy in range(int(h/2-120),int(h/2+120))) and activate_lock==0:

                        cv2.rectangle(frame,(int(7*w/8-60),int(h/2-120)),(int(7*w/8+60),int(h/2+120)),(0,0,255),5)
                        if  id==8:
                            pyautogui.PAUSE=0.75
                            cv2.putText(frame,'Play Pause here',(40,50),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),3)
                            pyautogui.press('playpause')

                    elif (cx in range(int(4*w/8-60),int(4*w/8+60))) and (cy in range(int(h/6-120),int(h/6+60))) and activate_lock==0:
                        cv2.putText(frame,'Manipulate Brightness here',(10,350),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
                        cv2.rectangle(frame,(int(4*w/8-60),int(h/6-120)),(int(4*w/8+60),int(h/6+60)),(0,255,0),5)
                        if id==8:
                            index_y1=cy
                            cv2.circle(frame,(cx,cy),5,(255,255,255),cv2.FILLED)

                        try:
                            if index_y1<t_cy:
                                sbc.set_brightness('+35')
                            elif index_y1>t_cy:
                                pyautogui.press('brightnessdown')
                                sbc.set_brightness('-35')

                            t_cy=index_y1
                        except:
                            print('Some kind of exception occured or idk')


                    elif (cx in range(int(4*w/8-260),int(4*w/8+260))) and (cy in range(int(h-120),int(h-25))) and activate_lock==0:
                        cv2.putText(frame,'Manipulate position here',(10,350),cv2.FONT_HERSHEY_PLAIN,3,(0,255,255),3)
                        cv2.rectangle(frame,(int(4*w/8-260),int(h-120)),(int(4*w/8+260),int(h-25)),(0,255,255),5)
                        pyautogui.PAUSE=0.005
                        if id==8:
                            index_x1=cx
                            cv2.circle(frame,(cx,cy),5,(255,255,255),cv2.FILLED)

                        try:
                            if index_x1<t_cx:
                                pyautogui.press('Right')

                            elif index_x1>t_cx:
                                pyautogui.press('left')
                            t_cx=index_x1
                        except:
                            print('Some kind of exception occured or idk')

                    elif (cx in range(int(w/2-100),int(w/2+100))) and (cy in range(int(h/2-100),int(h/2+100))):
                        cv2.rectangle(frame,(int(w/2-100),int(h/2-60)),(int(4*w/8+100),int(h/2+60)),(255,0,255),5)
                        if  id==8:
                            time.sleep(1.10)
                            activate_lock=0 if activate_lock==1 else 1
                            print(activate_lock)

                mpDraw.draw_landmarks(frame,handLms,mpHands.HAND_CONNECTIONS)
        cv2.putText(frame,'UnLocked' if activate_lock==0 else 'locked',(145,100),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv2.imshow('Gesture_Based_Controller',frame)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord('q'):
            break

if __name__=="__main__":
    main()
