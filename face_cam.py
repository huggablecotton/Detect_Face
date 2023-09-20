from getchar import Getchar
import cv2
import serial    
import timeit          
sp  = serial.Serial('COM10', 9600, timeout=1)
# 가중치 파일 경로
cascade_filename = 'haarcascade_frontalface_alt.xml'
# 모델 불러오기
cascade = cv2.CascadeClassifier(cascade_filename)

cam = cv2.VideoCapture(1)

pan = tilt = 76
_pan = _tilt = 10

_pan = pan
_tilt = tilt

margin_x = 30
margin_y = 30

def send_pan(pan):           
    tx_dat = "pan" + str(pan) + "\n"
    sp.write(tx_dat.encode())
    print(tx_dat)

def send_tilt(tilt):
    tx_dat = "tilt" + str(tilt) + "\n"
    sp.write(tx_dat.encode())
    print(tx_dat)

if not cam.isOpened():
    print("Could not open webcam")
    exit()
# 영상 검출기
def videoDetector(cam,cascade): 
       
    global pan; global _pan; global tilt; global _tilt;
    send_pan(76)
    send_tilt(45)
    kb = Getchar()
    key = ''
    
    while cam.isOpened():                                                   
       
        # 캡처 이미지 불러오기
        ret,img1 = cam.read()
        img = cv2.flip(img1, 1)
        # 영상 압축
        img = cv2.resize(img,dsize=None,fx=1.0,fy=1.0)
        # 그레이 스케일 변환
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        # cascade 얼굴 탐지 알고리즘 
        results = cascade.detectMultiScale(gray,            # 입력 이미지
                                           scaleFactor= 1.1,# 이미지 피라미드 스케일 factor
                                           minNeighbors=10,  # 인접 객체 최소 거리 픽셀
                                           minSize=(20,20)  # 탐지 객체 최소 크기
                                           )
                                                                        
        for box in results:
            x, y, w, h = box
            center_x = x + w//2
            center_y = y + h//2
            print("center = (%s, %s)" %(center_x, center_y))
            if center_x < 320 - margin_x:
                print("pan left")
                if pan - 2 >= 0:
                    pan = pan - 2
                    _pan = pan
                else:
                    pan = 0
                    _pan = pan
            elif center_x > 320 + margin_x:
                print("pan right")
                if pan + 2 <= 180:
                    pan = pan + 2
                    _pan = pan
                else:
                    pan = 180
                    _pan = pan
            else:
                print("pan stop")
                pan = _pan
            
            send_pan(pan) 
                
            if center_y < 240 - margin_y:
                print("tilt down")
                if tilt - 2 >= 0:
                    tilt = tilt - 2
                    _tilt = tilt
                else:
                    tilt = 0
                    _tilt = tilt
            elif center_y > 240 + margin_y:
                print("tilt up")
                if tilt + 2 <= 180:
                    tilt = tilt + 2
                    _tilt = tilt
                else:
                    tilt = 180
                    _tilt = tilt
            else:
                print("tilt stop")
                tilt = _tilt
                    
            send_tilt(tilt)
            
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), thickness=2)
     

         # 영상 출력        
        cv2.imshow('facenet',img)
        
        k = cv2.waitKey(5) & 0xFF
            
        if k == 27:
            break
       
            
    capture.release()
    cv2.destroyAllWindows()
# 영상 탐지기
videoDetector(cam,cascade)