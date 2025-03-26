# 01. 소벨 에지 검출 및 결과 시각화

- 이미지를 그레이스케일로 변환
- 소벨(Sobel) 필터를 사용해 X축과 Y축 방향의 에지를 검출
- 검출된 에지 강도(edge strength) 이미지를 시각화

    ### 요구사항
  
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
      - matplotlib를 사용해 원본 이미지와 에지강도 이미지를 나란히시각화
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
  ### 결과 화면
      ![image](https://github.com/user-attachments/assets/a10555c1-a931-400a-b76f-1d7817a023a6)

      
