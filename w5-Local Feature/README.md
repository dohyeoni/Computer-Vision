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
            bf_match = bf_matcher.match(des1, des2)
            
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params = dict(checks=50)
            
            flann_matcher = cv.FlannBasedMatcher(index_params, search_params)    # FlannBasedMatcher() 사용
            flann_knn_match = flann_matcher.knnMatch(des1, des2, k=2)
            
            T=0.7
            bf_good_match = []
            for match in bf_match:
                bf_good_match.append(match)
            print('BF 매칭에 걸린 시간: ', time.time()-start)
            
            falnn_good_match = []
            for nearest1, nearest2 in flann_knn_match:
                if(nearest1.distance/nearest2.distance)<T:
                    falnn_good_match.append(nearest1)
            print('Flann 매칭에 걸린 시간: ', time.time()-start)
            
            
           
      ```
    - cv.drawMatches()를 사용하여 매칭결과 시각화
      ```python
               img_match = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype=np.uint8)
            bf_img = cv.drawMatches(img1, kp1, img2, kp2, bf_good_match, img_match, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            flann_img = cv.drawMatches(img1, kp1, img2, kp2, falnn_good_match, img_match, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

      ```
    - matplotlib를 사용해 원본 이미지와 직선이 그려진 이미지를 나란히 시각화
      ```python
            plt.figure(figsize=(10, 5))

            plt.subplot(1, 2, 1)
            plt.imshow(cv.cvtColor(bf_img, cv.COLOR_BGR2RGB))
            plt.title('BFMatcher')
            plt.axis('off')
            
            plt.subplot(1, 2, 2)
            plt.imshow(cv.cvtColor(flann_img, cv.COLOR_BGR2RGB))
            plt.title('FlannBasedMatcher')
            plt.axis('off')
            
            plt.show()
      ```

  #### 결과 화면
  ![image](https://github.com/user-attachments/assets/5a2c79f1-662c-41dd-9619-969343484cb2)


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


