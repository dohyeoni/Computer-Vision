import cv2 as cv
import sys
import numpy as np

#######################################################################
# 01 이미지 불러오기 및 그레이스케일 변환 
# src_img = cv.imread('soccer.jpg')       # soccer.jpg 이미지 읽기기

# if src_img is None:
#     sys.exit('파일이 존재하지 않습니다.')
    
# result_img = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)    # 흑백 변환(BGR->GRAY)

# # 이미지 array로 변환환 
# a = np.array(src_img)
# b = np.array(result_img)

# b = cv.cvtColor(b, cv.COLOR_GRAY2BGR)   # 흑백 이미지를 3채널로 변환 

# c = np.hstack((a, b))

# cv.imshow('Image Display', c)

# # Image Display라는 창을 키보드 입력이 들어올 때까지 켜놓기
# cv.waitKey()
# cv.destroyAllWindows()


# # Image Display 창이 꺼지면 img의 type과 shape를 출력함
# print(type(src_img))
# print(src_img.shape)





###################################################################################3
# 02웹캠 영상에서 에지 검출 #
# cap = cv.VideoCapture(0, cv.CAP_DSHOW)  # 카메라와 연결 시도

# if not cap.isOpened():
#     sys.exit('카메라 연결 실패')
    
# while True:
#     ret, frame = cap.read()
    
#     if not ret:     # 카메라로 부터 프레임을 성공적으로 읽었는지를 나타내는 변수
#         print('프레임 획득에 실패하여 루프를 나갑니다.')
#         break
    
#     gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
#     a = np.array(frame)
#     b = cv.Canny(gray_frame, 100, 200)
    
#     b = cv.cvtColor(b, cv.COLOR_GRAY2BGR)
    
#     c = np.hstack((a,b))
    
#     cv.imshow('Image Display', c)

#     key = cv.waitKey(1)     # 1밀리초 동안 키보드 입력 기다림
    
#     if key == ord('q'):     # 'q' 키가 들어오면서 루프를 빠져나감
#         break
    
# cap.release()           # 카메라와 연결을 끊음
# cv.destroyAllWindows()  # 윈도우창 종료





# #################################################################################3
# # 03마우스로 영역 선택 및 ROI(관심영역) 추출 #
original_img = cv.imread('soccer.jpg')       # soccer.jpg 이미지 읽기

if original_img is None:
    sys.exit('파일이 존재하지 않습니다.')
    
img = original_img.copy()    

# 드래그 상태 및 좌표 변수
drawing = False     # 드래그 상태 확인
ix, iy =  -1, -1    # 시작 좌표
ROI = None
    
def draw(event, x, y, flags, param):        # 콜백 함수
    global ix, iy, drawing, img, ROI
    
    if event == cv.EVENT_LBUTTONDOWN:       # 마우스 왼쪽 버튼 클릭(down)했을 때 -> 초기 위치 저장
        drawing = True
        ix, iy = x,y
    
    elif event == cv.EVENT_MOUSEMOVE: # 마우스 이동 중
        if drawing:
            tmp_img = img.copy()
            cv.rectangle(tmp_img, (ix,iy), (x,y), (0,0,255), 2)
            cv.imshow('Drawing', tmp_img)
            
    elif event == cv.EVENT_LBUTTONUP:     # 마우스 왼쪽 버튼 클릭(up)했을 때 
        drawing = False
        cv.rectangle(img, (ix,iy), (x, y), (0, 0, 255), 2)
        cv.imshow('Drawing', img)
        
        # numpy로 ROI 추출
        x1, y1 = min(ix, x), min(iy, y)
        x2, y2 = max(ix, x), max(iy, y)
        ROI = img[y1:y2, x1:x2]
        
        # ROI 별도의 창에 출력
        if ROI.shape[0] > 0 and ROI.shape[1] > 0:
            cv.imshow('ROI', ROI)

cv.namedWindow('Drawing')
cv.imshow('Drawing', img)
cv.setMouseCallback('Drawing', draw)    # Drawing 윈도우에 draw 콜백 함수 지정

while(True):        # 마우스 이벤트가 언제 발생할지 모르므로 무한 반복
    if cv.waitKey(1) == ord('q'):       # q키를 눌러 종료료
        cv.destroyAllWindows()
        break
    
    elif cv.waitKey(1) == ord('r'):     # r키를 눌러 영역 선택 리셋 
        img = original_img.copy()
        ROI = None
        cv.imshow('Drawing', img)
    
    elif cv.waitKey(1) == ord('s'):     # s키를 눌러 선택한 영역을 이미지 파일로 저장 
        if ROI is not None and ROI.shape[0] > 0 and ROI.shape[1] > 0:
            cv.imwrite('ROI.jpg', ROI)
            print('ROI가 저장됨')