# 01.  SORT 알고리즘을 활용한 다중 객체 추적기 구현

- SORT 알고리즘을 사용하여 비디오에서 다중 객체를 실시간으로 추적하는 프로그램 구현하기

    #### 요구사항
    - 객체 검출기 구현: YOLOv4와 같은 사전 훈련된 객체 검출 모델을 사용하여 각 프레임에서 객체를 검출한다.
      ```python
           def construct_yolo_v4():
                f = open('coco_names.txt', 'r')
                class_name = [line.strip() for line in f.readlines()]
                
                model = cv.dnn.readNet('yolov4.weights', 'yolov4.cfg')
                layer_name = model.getLayerNames()
                out_layers = [layer_name[i-1] for i in model.getUnconnectedOutLayers()]
                
                return model, out_layers, class_name
            
            def yolo_detect(img, yolo_model, out_layers):
                height, width = img.shape[0], img.shape[1]
                test_img = cv.dnn.blobFromImage(img, 1.0/256, (448,448), (0,0,0), swapRB=True)
                
                yolo_model.setInput(test_img)
                output3 = yolo_model.forward(out_layers)
                
                box, conf, id = [], [], []
                for output in output3:
                    for vec85 in output:
                        scores = vec85[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        if confidence>0.5:
                            centerx, centery = int(vec85[0]*width), int(vec85[1]*height)
                            w, h =int(vec85[2]*width), int(vec85[3]*height)
                            x, y = int(centerx-w/2), int(centery-h/2)
                            box.append([x,y,x+w, y+h])
                            conf.append(float(confidence))
                            id.append(class_id)
                            
                ind = cv.dnn.NMSBoxes(box, conf, 0.5, 0.4)
                objects = [box[i]+[conf[i]]+[id[i]] for i in range(len(box)) if i in ind]
                return objects
            
            model, out_layers, class_names = construct_yolo_v4()


      ```
    - mathworks.comSORT 추적기 초기화: 검출된 객체의 경계 상자를 입력으로 받아 SORT 추적기를 초기화 한다.
      ```python
              # 데이터 불러오기
              (x_train, y_train), (x_test, y_test) = mnist.load_data()
      ```
    - 객체 추적: 각 프레임마다 검출된 객체와 기존 추적 객체를 연관시켜 추적을 유지한다.
      ```python
                model = Sequential([
                Dense(128, activation='relu', input_shape=(784,)),  # 은닉층
                Dense(10, activation='softmax')                     # 출력층: 숫자 0~9
            ])  
      ```
    - 결과 시각화: 추적된 각 객체에 고유 ID를 부여하고, 해당 ID와 경계 상자를 비디오 프레임에 표시하여 실시간으로 출력한다.
      ```python
              model.fit(x_train, y_train, epochs=5, batch_size=32, validation_split=0.1)

      ```
          
  #### 결과 화면
  ![image](https://github.com/user-attachments/assets/2ab9c735-c8d4-40ce-9b46-657c1cd51329)
  ![image](https://github.com/user-attachments/assets/ff77f374-650d-4126-bcc2-e34dbba37bec)




---
      
# 02. Mediapipe를 활용한 얼굴 랜드마크 추출 및 시각화

- Mediapipe의 FaceMesh 모듈을 사용하여 얼굴의 468개 랜드마크를 추출하고, 이를 실시간 영상에 시각화하는 프로그램 구현하기

    #### 요구사항
    - Mediapipe의 FaceMesh 모듈을 사용하여 얼굴 랜드마크 검출기를 초기화 한다.
       ```python
                import tensorflow as tf
                from tensorflow import keras
                from keras.datasets import cifar10
       ```
    - OpenCV를 사용하여 웹캠으로부터 실시간 영상을 캡처한다.
      ```python
              train_images, test_images= train_images/ 255.0, test_images/ 255.0
      ```
    - 검출된 얼굴 랜드마크를 실시간 영상에 점으로 표시한다.
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
    - ESC 키를 누르면 프로그램이 종료되도록 설정한다.
      ```python
               test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=2)

                # 5개 테스트 이미지에 대한 예측
                predictions = model.predict(test_images[:5])
                
                plt.figure(figsize=(15, 3))
                
                for i in range(5):
                    plt.subplot(1, 5, i + 1)
                    plt.imshow(test_images[i])
                    plt.title(f"prediction: {class_names[np.argmax(predictions[i])]}")
                    plt.axis('off')
                    
                plt.tight_layout()
                plt.show()
            
      ```


  #### 결과 화면
  ![image](https://github.com/user-attachments/assets/1e69bc71-302c-4452-ade7-a278ebc5f9d0)
  ![image](https://github.com/user-attachments/assets/cae74182-60ba-43ed-8742-b15a6ff88d16)




---
