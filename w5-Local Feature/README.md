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
              sift = cv.SIFT_create(nfeatures=100)
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
  - SIFT_create() 매개변수 nfeatures=100으로 제한한 경우
  ![image](https://github.com/user-attachments/assets/26d0d447-e43e-400f-8c16-f048e4f683b6)

  +) 원 크기의 의미: 원 크기는 특징점이 유효하게 검출된 지역의 크기를 의미한다.
  ![image](https://github.com/user-attachments/assets/5a6db344-4972-4e24-80be-aa6d4738829c)
  (출처: https://docs.opencv.org/4.x/da/df5/tutorial_py_sift_intro.html)

  


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
    - cv.drawMatches()를 사용하여 매칭결과 시각화
      ```python
            img_match = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype=np.uint8)
            bf_img = cv.drawMatches(img1, kp1, img2, kp2, bf_good_match, img_match, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            flann_img = cv.drawMatches(img1, kp1, img2, kp2, falnn_good_match, img_match, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

      ```
     
    - matplotlib을 이용하여 매칭결과 출력
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
  ![image](https://github.com/user-attachments/assets/591de309-06f5-44a7-a597-5b37b3b21356)



---
      
# 03. 호모그래피를 이용한 이미지 정합(Image Alignment)

- SIFT 특징점을 사용하여 두 이미지간 대응점을 찾고, 호모그래피를 계산하여 하나의 이미지 위에 정렬하기

    #### 요구사항
    - cv.imread()를 사용하여 두 개의 이미지 불러오기
       ```python
            img1 = cv.imread('img1.jpg')
            gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
            img2 = cv.imread('img2.jpg')
            gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
       ```
    - cv.SIFT_create()를 사용하여 특징점 추출
      ```python
              sift = cv.SIFT_create()
      ```
    - cv.BFMatcher()를 사용하여 특징점을 매칭 
      ```python
            bf_matcher = cv.BFMatcher(cv.NORM_L2, crossCheck=False)
            bf_knn_match = bf_matcher.knnMatch(des1, des2, k=2)
            
            T=0.7
            bf_good_match = []
            for nearest1, nearest2 in bf_knn_match:
                if(nearest1.distance/nearest2.distance)<T:
                    bf_good_match.append(nearest1)
                    
                    
            img_match = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype=np.uint8)
            bf_img = cv.drawMatches(img1, kp1, img2, kp2, bf_good_match, img_match, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

      ```
    - cv.findHomography()를 사용하여 호모그래피 행렬을 계산
      ```python
            points1 = np.float32([kp1[m.queryIdx].pt for m in bf_good_match])    # queryIdx - img1의 매칭된 키포인트 인덱스
            points2 = np.float32([kp2[m.trainIdx].pt for m in bf_good_match])    # trainIdx - img2의 매칭된 키포인트 인덱스
            
            H,_= cv.findHomography(points1, points2, cv.RANSAC))
      ```
    - cv.warpPerspective()를 사용하여 한 이미지를 변환하여 다른 이미지와 정렬
      ```python
            h1, w1 = img1.shape[:2] # img1의 세로(h1), 가로(w1) 크기를 가져옴 -> 이미지의 모서리 좌표를 지정하기 위해 필요 
            corners1 = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]]).reshape(-1, 1, 2)   #img1의 네 모서리를 H 행렬로 변형 
            transformed_corners1 = cv.perspectiveTransform(corners1, H) # img1이 img2 시점으로 어떻게 왜곡되는지 계산 -> 정렬된 img1의 네 모서리 좌표가 반환됨 
            
            
            h2, w2 = img2.shape[:2] # img2의 모서리도 정의 
            corners2 = np.float32([[0, 0], [w2, 0], [w2, h2], [0, h2]]).reshape(-1, 1, 2)
            
            # 두 이미지의 전체 범위를 감싸는 새로운 캔버스 크기 계산 
            all_corners = np.concatenate((transformed_corners1, corners2), axis=0)  # 변환된 img1의 모서리 + img2의 모서리 => 전체를 감싸는 새로운 범위를 계산하기 위함 
            [x_min, y_min] = np.int32(all_corners.min(axis=0).ravel() - 10)
            [x_max, y_max] = np.int32(all_corners.max(axis=0).ravel() + 10)
            
            # 평행이동 변환 행렬 적용 (좌표가 음수가 되지 않도록) 
            new_width = x_max - x_min
            new_height = y_max - y_min
            
            translation_matrix = np.array([[1, 0, -x_min], [0, 1, -y_min], [0, 0, 1]]) 
            H_translated = translation_matrix @ H   # 기존 호모그래피 H에 translation을 곱해서 -> 최종적으로 이미지 정합을 할 때 음수 좌표를 피하고 + 새로운 캔버스 상에서 정확히 맞춰주는 행렬
            
            img1_aligned = cv.warpPerspective(img1, H_translated, (new_width, new_height))

      ```
    - 변환된 이미지를 원본 이미지와 비교하여 출력
      ```python
            plt.figure(figsize=(18, 8))

            plt.subplot(1, 4, 1)
            plt.imshow(cv.cvtColor(img1, cv.COLOR_BGR2RGB))
            plt.title('img1.jpg')
            plt.axis('off')
            
            plt.subplot(1, 4, 2)
            plt.imshow(cv.cvtColor(img2, cv.COLOR_BGR2RGB))
            plt.title('img2.jpg')
            plt.axis('off')
            
            plt.subplot(1, 4, 3)
            plt.imshow(cv.cvtColor(blend, cv.COLOR_BGR2RGB))
            plt.title('Alignment')
            plt.axis('off')
            
            plt.subplot(1, 4, 4)
            plt.imshow(cv.cvtColor(bf_img, cv.COLOR_BGR2RGB))
            plt.title('BFMatcher')
            plt.axis('off')

      ```


  #### 결과 화면
  ![image](https://github.com/user-attachments/assets/10bcfb4c-5544-4b6d-999b-30887db67a48)
  ![image](https://github.com/user-attachments/assets/d05bdd99-7705-4880-a062-0ba8e3733fdf)




