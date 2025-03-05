# 01 이미지 불러오기 및 그레이스케일 변환 
- OpenCV를 사용하여 이미지를 불러오고 화면에 출력한다.
- 원본 이미지와 그레이스케일로 변환된 이미지를 나란히 표시한다.

input img
![soccer](https://github.com/user-attachments/assets/bdcf6215-f6ae-4ae1-8338-d4ea90fbe6f9)

output 
![스크린샷 2025-03-05 105655](https://github.com/user-attachments/assets/310d0b2b-4957-4487-bc3f-68ed4796bbbc)

- cv.imread()를 사용해 이미지 로드
  ```python
  src_img = cv.imread('soccer.jpg')
  ```
- cv.cvtColor() 함수를 사용해 이미지를 그레이스케일로 변환
  ```python
  result_img = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)
  ```
- np.stack() 함수를 이용해 원본 이미지와 그레이스케일 이미지를 가로로 연결해 출력  
  ```python
    a = np.array(src_img)
    b  = np.array(result_img)

    b = cv.cvtColor(b, cv.COLOR_GRAY2BGR)   # 흑백 이미지를 3채널로 변환 

    c = np.hstack((a, b))
    cv.imshow('Image Display', c)
  ```

- cv.imshow()와 cv.waitKey()를 사용해 결과를 화면에 표시하고, 아무 키나 누르면 창이 닫히도록 함
  ```python
  cv.imshow('Image Display', c)
  cv.waitKey()
  ```

## 02 웹캠 영상에서 에지 검출
- 웹캠을 사용하여 실시간 비디오 스트림을 가져온다.
- 각 프레임에서 Canny Edge Detection을 적용하여 에지를검출하고 원본 영상과 함께 출력한다.
![스크린샷 2025-03-04 210749](https://github.com/user-attachments/assets/d33e907b-28f4-4a63-839e-a6856d1277ea)


- cv.VideoCaapture()를 사용해 웹캠 영상을 로드
  ```python
  cap = cv.VideoCapture(0, cv.CAP_DSHOW)
  ```

- 각 프레임을 그레이스케일로 변환 후, cv.Canny()함수를 사용해 에지 검출 수행
   ```python
   gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
   a = np.array(frame)
   b = cv.Canny(gray_frame, 100, 200)
  ```
- 원본 영상과 에지 검출 영상을 가로로 연결해 화면에 출력
   ```python
   c = np.hstack((a,b))
    
   cv.imshow('Image Display', c)
  ```
- 'q' 키를 누르면 영상 창이 종료
  ```python
    while True:
  
     key = cv.waitKey(1)     
    
     if key == ord('q'):     
         break
    
   cap.release()           
   cv.destroyAllWindows()
  ```


## 03 마우스로 영역 선택 및 ROI(관심영역) 추출
- 이미지를 불러오고 사용자가 마우스로 클릭하고 드래그하여 관심영역(ROI)을 선택한다.
- 선택한 영역만 따로 새로운 창에 출력하고, 저장한다.

- 이미지를 불러오고 화면에 출력
  ```python
   original_img = cv.imread('soccer.jpg')
  ```



- cv.setMouseCallback()을 사용하여 마우스 이벤트 처리
  ```python
   def draw(event, x, y, flags, param):        
  ```
- 사용자가 클릭한 시작점에서 드래그에하여 사각형을 그리며 영역을 선택
 ```python
   def draw(event, x, y, flags, param):        
    global ix, iy, drawing, img, ROI
    
    if event == cv.EVENT_LBUTTONDOWN:       
        drawing = True
        ix, iy = x,y
    
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            tmp_img = img.copy()
            cv.rectangle(tmp_img, (ix,iy), (x,y), (0,0,255), 2)
            cv.imshow('Drawing', tmp_img)
  ```
![스크린샷 2025-03-05 105359](https://github.com/user-attachments/assets/8cef5bc7-672b-447b-8080-c8cdf1b71c9a)
![스크린샷 2025-03-05 105409](https://github.com/user-attachments/assets/96b8e2fc-7c23-435e-8a2b-c0e03210ff2b)

- 마우스를 놓으면 해당 영역을 잘라내서 별도의 창에 출력
 ```python
   # ROI 별도의 창에 출력
        if ROI.shape[0] > 0 and ROI.shape[1] > 0:
            cv.imshow('ROI', ROI)
  ```
![image](https://github.com/user-attachments/assets/db891a9b-e3cd-4df9-933a-45d21970afac)

- 'r'키를 누르면 영역 선택을 리셋하고 처음부터 다시 선택
- 's'키를 누르면 선택한 영역을 이미지 파일로 저장
  ```python
   while(True):        
    if cv.waitKey(1) == ord('q'):      
        cv.destroyAllWindows()
        break
    
    elif cv.waitKey(1) == ord('r'):     
        img = original_img.copy()
        ROI = None
        cv.imshow('Drawing', img)
    
    elif cv.waitKey(1) == ord('s'):     
        if ROI is not None and ROI.shape[0] > 0 and ROI.shape[1] > 0:
            cv.imwrite('ROI.jpg', ROI)
            print('ROI가 저장됨')
  ```
![스크린샷 2025-03-05 105439](https://github.com/user-attachments/assets/e804cf30-eff9-4d86-a046-9a947116a3d9)
![스크린샷 2025-03-05 105424](https://github.com/user-attachments/assets/f76ce821-68b6-49ea-9ad6-b25ce2b95446)

