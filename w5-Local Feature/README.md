# 01.  SIFT를 이용한 특징점 검출 및 시각화

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
      
# 02. SIFT를 이용한 두 영상 간 특징점 매칭

- 두 개의 이미지를 입력받아 SIFT 특징점 기반으로 매칭을 수행하고 결과를 시각화하기

    #### 요구사항
    - cv.imread()를 사용하여 두 개의 이미지 불러오기
       ```python
              img1 = cv.imread('mot_color70.jpg')[190:350, 440:560]
              gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
              img2 = cv.imread('mot_color83.jpg')
              gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
       ```
    - cv.SIFT_create()를 사용하여 특징점 추출
      ```python
              sift = cv.SIFT_create()
      ```
    - cv.BFMatcher() 또는 cv.FlannBasedMatcher()를 사용하여 두 영상 간 특징점 매칭
      ```python
            bf_matcher = cv.BFMatcher(cv.NORM_L2, crossCheck=True)
            bf_match = bf_matcher.match(체
  ![image](https://github.com/user-attachments/assets/9a226d07-96ca-4420-a827-3e28461f2d0a)



