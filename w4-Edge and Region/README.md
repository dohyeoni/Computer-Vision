# 01. 소벨 에지 검출 및 결과 시각화

- 이미지를 그레이스케일로 변환
- 소벨(Sobel) 필터를 사용해 X축과 Y축 방향의 에지를 검출
- 검출된 에지 강도(edge strength) 이미지를 시각화

    #### 요구사항
    - cv.imread()를 사용해 이미지 불러오기
          ```python
              img = cv.imread('soccer.jpg')
          ```
    - cv.cvtColor()를 사용해 그레이스케일로 변환
          ```python
              gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
          ```
    - cv.Sobel()을 사용해 X축(cv.CV_64F, 1, 0)과 Y축(cv.CV_64F, 0, 1) 방향의 에지를 검출
          ```python
              grad_x = cv.Sobel(gray, cv.CV_64F, 1, 0, ksize=3)   # 소벨 연산자 적용
              grad_y = cv.Sobel(gray, cv.CV_64F, 0, 1, ksize=3)
          ```
    - cv.magnitude()를 사용해 에지강도 계산
          ```python
              mag = cv.magnitude(grad_x, grad_y)
          ```
    - matplotlib를 사용해 원본 이미지와 에지강도 이미지를 나란히 시각화
          ```python
              mag_img = cv.convertScaleAbs(mag)   

              plt.figure(figsize=(10, 5))
                
              plt.subplot(1, 2, 1)
              plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
              plt.title('Original')
              plt.axis('off')
                
              plt.subplot(1, 2, 2)
              plt.imshow(mag_img, cmap='gray')
              plt.title('Edge Magnitude')
              plt.axis('off') 
          ```
          
  #### 결과 화면
      ![image](https://github.com/user-attachments/assets/a10555c1-a931-400a-b76f-1d7817a023a6)

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
          ```python
              cv.grabCut(src, mask, (x, y, w, h), bgdModel, fgdModel, iterCount, mode)
          ```
     - 초기 사각형 영역은 (x, y, width, height) 형식으로 설정
           ```python
              canny = cv.Canny(gray, 100, 200)
          ```
     - 마스크를 사용해 원본 이미지에서 배경 제거
           ```python
              canny = cv.Canny(gray, 100, 200)
          ```
     - matplotlib를 사용해 원본이미지, 마스크 이미지, 배경 제거 이미지 세 개를 나란히 시각화
           ```python
              canny = cv.Canny(gray, 100, 200)
          ```
  
