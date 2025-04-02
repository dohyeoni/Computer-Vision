# 01.  SIFT를 이용한특징점검출및시각화

- SIFT 알고리즘을 사용하여 특징점을 검출하고 시각화하기

    #### 요구사항
    - cv.imread()를 사용해 이미지 불러오기
      ```python
              img = cv.imread('soccer.jpg')
      ```
    - cv.SIFT_create()를 사용하여 SIFT 객체 생성
      ```python
              sift = cv.SIFT_create()
      ```
    - detectAndCompute()를 사용하여 특징점 검출
      ```python
              kp, des = sift.detectAndCompute(gray, None)    
      ```
    - cv.drawKeypoints()를 사용하여 특징점 이미지에 시각화
      ```python
              gray = cv.drawKeypoints(gray, kp, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)    # 특징점을 이미지에 시각화
      ```
    - matplotlib를 사용해 원본 이미지와 특징점이시각화된이미지를나란히출력
      ```python
              plt.figure(figsize=(10, 5))

              plt.subplot(1, 2, 1)
              plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
              plt.title('Original')
              plt.axis('off')
              
              plt.subplot(1, 2, 2)
              plt.imshow(gray)
              plt.title('sift')
              plt.axis('off')
              
              plt.show()
      ```
          
  #### 결과 화면
  ![image](https://github.com/user-attachments/assets/0e5138a2-633b-4a8a-8d69-e05b1798c0f9)


---
      
# 02. 캐니 에지 및 허프 변환을 이용한 직선 검출

- 캐니(Canny) 에지검출을 사용해 에지맵을 생성
- 허프변환(Hough Transform)을 사용해 이미지에서 직선을 검출
- 검출된 직선을 원본이미지에 빨간색으로 표시

    #### 요구사항
    - cv.Canny()를 사용해 에지맵 생성
       ```python
              canny = cv.Canny(gray, 100, 200)
       ```
    - cv.HoughLinesP()를 사용해 직선을 검출
      ```python
              lines = cv.HoughLinesP(canny, 1, np.pi/180, 50, minLineLength=10, maxLineGap=1)
      ```
    - cv.line()을 사용해 검출된 직선을 원본 이미지에 그리기
      ```python
              if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2, cv.LINE_AA)
      ```
    - matplotlib를 사용해 원본 이미지와 직선이 그려진 이미지를 나란히 시각화
      ```python
              plt.subplot(1, 2, 1)
              plt.imshow(gray, cmap='gray')
              plt.title('Original')
              plt.axis('off')
            
              plt.subplot(1, 2, 2)
              plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
              plt.title('Hough Lines')
              plt.axis('off')
            
              plt.show()
      ```

  #### 결과 화면
  ![image](https://github.com/user-attachments/assets/24395420-67bc-433a-b08e-681388f758a5)

---

# 03. GrabCut을 이용한 대화식 영역 분할 및 객체 추출
- 사용자가 지정한 사각형 영역을 바탕으로 GrabCut 알고리즘을 사용해 객체를 추출
- 객체 추출 결과를 마스크 형태로 시각화
- 원본 이미지에서 배경을 제거하고 객체만 남은 이미지를 출력

    #### 요구사항
     - cv.grabCut()를 사용해 대화식 분할을 수행
     - 초기 사각형 영역은 (x, y, width, height) 형식으로 설정
       ```python
            src = skimage.data.coffee()
            mask = np.zeros(src.shape[:2], np.uint8)
            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)
            iterCount = 1
            mode = cv.GC_INIT_WITH_RECT
            rc = (100, 100, 200, 200)
            
            cv.grabCut(src, mask, rc, bgdModel, fgdModel, iterCount, mode)
       ```
     - 마스크를 사용해 원본 이미지에서 배경 제거
       ```python
            mask2 = np.where((mask == 0) | (mask == 2), 0, 1).astype('uint8')
            dst = src * mask2[:, :, np.newaxis]
            
            cv.imshow('dst', dst)
            
            def on_mouse(event, x, y, flags, param):
                if event == cv.EVENT_LBUTTONDOWN:
                    cv.circle(dst, (x, y), 3, (255, 0, 0), -1)
                    cv.circle(mask, (x, y), 3, cv.GC_FGD, -1)
                    cv.imshow('dst', dst)
                elif event == cv.EVENT_RBUTTONDOWN:
                    cv.circle(dst, (x, y), 3, (0, 0, 255), -1)
                    cv.circle(mask, (x, y), 3, cv.GC_BGD, -1)
                    cv.imshow('dst', dst)
                elif event == cv.EVENT_MOUSEMOVE:
                    if flags & cv.EVENT_FLAG_LBUTTON:
                        cv.circle(dst, (x, y), 3, (255, 0, 0), -1)
                        cv.circle(mask, (x, y), 3, cv.GC_FGD, -1)
                        cv.imshow('dst', dst)
                    elif flags & cv.EVENT_FLAG_RBUTTON:
                        cv.circle(dst, (x, y), 3, (0, 0, 255), -1)
                        cv.circle(mask, (x, y), 3, cv.GC_BGD, -1)
                        cv.imshow('dst', dst)
                        
            cv.setMouseCallback('dst', on_mouse)
       ```
     - matplotlib를 사용해 원본이미지, 마스크 이미지, 배경 제거 이미지 세 개를 나란히 시각화
       ```python
             plt.figure(figsize=(15, 5))

            plt.subplot(1, 3, 1)
            plt.imshow(cv.cvtColor(src, cv.COLOR_BGR2RGB))
            plt.title('Original')
            plt.axis('off')
            
            plt.subplot(1, 3, 2)
            plt.imshow(mask, cmap='gray')
            plt.title('Mask')
            plt.axis('off')
            
            plt.subplot(1, 3, 3)
            plt.imshow(cv.cvtColor(dst, cv.COLOR_BGR2RGB))
            plt.title('Background Removed')
            plt.axis('off')

            plt.show()
       ```

  #### 결과 화면
  ![image](https://github.com/user-attachments/assets/f3cf3954-47b0-4c5e-b0aa-df23e3de0310)


