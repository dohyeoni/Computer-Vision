# 01.  간단한 이미지 분류기 구현

- MNIST 데이터 셋(손글씨 숫자 이미지)을 이용하여 간단한 이미지 분류기 구현하기

    #### 요구사항
    - MNIST 데이터셋 로드
      ```python
              import tensorflow as tf
              from tensorflow.keras.datasets import mnist


      ```
    - 데이터 훈련 세트와 테스트 세트로 분할
      ```python
              # 데이터 불러오기
              (x_train, y_train), (x_test, y_test) = mnist.load_data()
      ```
    - 간단한 신경망 모델 구축
      ```python
                model = Sequential([
                Dense(128, activation='relu', input_shape=(784,)),  # 은닉층
                Dense(10, activation='softmax')                     # 출력층: 숫자 0~9
            ])  
      ```
    - 모델을 훈련시키고 정확도 평가하기
      ```python
              model.fit(x_train, y_train, epochs=5, batch_size=32, validation_split=0.1)

      ```
          
  #### 결과 화면
  


---
      
# 02. CIFAR-10 데이터셋을 활용한 CNN 모델 구축

- CIFAR-10 데이터셋을 활용하여 CNN을 구축하고, 이미지 분류를 수행

    #### 요구사항
    - CIFAR-10 데이터셋 로드
       ```python
              img1 = cv.imread('mot_color70.jpg')[190:350, 440:560]
              gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
              img2 = cv.imread('mot_color83.jpg')
              gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
       ```
    - 데이터 전처리(정규화 등) 수행
      ```python
              sift = cv.SIFT_create()
      ```
    - CNN 모델을 설계하고 훈련하기기
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
    - 모델의 성능을 평가하고, 테스트 이미지에 대한 예측 수행하기
      ```python
            
      ```


  #### 결과 화면


---
