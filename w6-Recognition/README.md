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
  ![image](https://github.com/user-attachments/assets/2ab9c735-c8d4-40ce-9b46-657c1cd51329)



---
      
# 02. CIFAR-10 데이터셋을 활용한 CNN 모델 구축

- CIFAR-10 데이터셋을 활용하여 CNN을 구축하고, 이미지 분류를 수행

    #### 요구사항
    - CIFAR-10 데이터셋 로드
       ```python
                import tensorflow as tf
                from tensorflow import keras
                from keras.datasets import cifar10
       ```
    - 데이터 전처리(정규화 등) 수행
      ```python
              train_images, test_images= train_images/ 255.0, test_images/ 255.0
      ```
    - CNN 모델을 설계하고 훈련하기기
      ```python
            model = models.Sequential()

            model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
            model.add(layers.MaxPooling2D((2, 2)))
            model.add(layers.Conv2D(64, (3, 3), activation='relu'))
            model.add(layers.MaxPooling2D(2, 2))
            model.add(layers.Conv2D(64, (3, 3), activation='relu'))
            
            model.add(layers.Flatten())
            model.add(layers.Dense(64, activation='relu'))
            model.add(layers.Dropout(0.5))  # 50% 뉴런 비활성화
            model.add(layers.Dense(10, activation='softmax'))
            
            model.summary()
            
            model.compile(optimizer='adam',
                          loss='sparse_categorical_crossentropy',
                          metrics=['accuracy'])
            
            model.fit(train_images, 
                      train_labels, 
                      epochs=15,
    - 모델의 성능을 평가하고, 테스트 이미지에 대한 예측 수행하기
      ```python
              test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=2)
            
      ```


  #### 결과 화면


---
