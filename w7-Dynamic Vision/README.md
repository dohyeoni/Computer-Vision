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
                detected_objects = [res[i] for i in range(len(res)) if res[i][5] in [0,2]]
    
                if len(detected_objects)==0:
                    tracks = sort.update()
                else:
                    tracks=sort.update(np.array(detected_objects))
      ```
    - 객체 추적: 각 프레임마다 검출된 객체와 기존 추적 객체를 연관시켜 추적을 유지한다.
      ```python
                tracks=sort.update(np.array(detected_objects))
      ```
    - 결과 시각화: 추적된 각 객체에 고유 ID를 부여하고, 해당 ID와 경계 상자를 비디오 프레임에 표시하여 실시간으로 출력한다.
      ```python
              for i in range(len(tracks)):
                x1, y1, x2, y2, track_id = tracks[i].astype(int)
                cv.rectangle(frame, (x1,y1), (x2,y2), colors[track_id], 2)
                cv.putText(frame, str(track_id), (x1+10, y1+40), cv.FONT_HERSHEY_PLAIN, 3, colors[track_id], 2)

      ```
          
  #### 결과 화면
  ![스크린샷 2025-04-16 110627](https://github.com/user-attachments/assets/c6b2c4ae-ffcf-481c-9c25-988f92a25101)
  ![스크린샷 2025-04-16 110700](https://github.com/user-attachments/assets/ba49ea07-23c6-4f72-871a-43d20e95508f)





---
      
# 02. Mediapipe를 활용한 얼굴 랜드마크 추출 및 시각화

- Mediapipe의 FaceMesh 모듈을 사용하여 얼굴의 468개 랜드마크를 추출하고, 이를 실시간 영상에 시각화하는 프로그램 구현하기

    #### 요구사항
    - Mediapipe의 FaceMesh 모듈을 사용하여 얼굴 랜드마크 검출기를 초기화 한다.
       ```python
                mp_mesh = mp.solutions.face_mesh
                mp_drawing = mp.solutions.drawing_utils
                mp_styles = mp.solutions.drawing_styles
                
                mesh = mp_mesh.FaceMesh(max_num_faces=2, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
       ```
    - OpenCV를 사용하여 웹캠으로부터 실시간 영상을 캡처한다.
      ```python
              cap = cv.VideoCapture(0, cv.CAP_DSHOW)
      ```
    - 검출된 얼굴 랜드마크를 실시간 영상에 점으로 표시한다.
      ```python
                if res.multi_face_landmarks:
                    for landmarks in res.multi_face_landmarks:
                        mp_drawing.draw_landmarks(image=frame, 
                                                  landmark_list=landmarks, 
                                                  connections=mp_mesh.FACEMESH_TESSELATION, 
                                                  landmark_drawing_spec=None, 
                                                #   connection_drawing_spec=mp_styles.get_default_face_mesh_tesselation_style()
                                                )
                        
                        mp_drawing.draw_landmarks(image=frame, 
                                                  landmark_list=landmarks, 
                                                  connections=mp_mesh.FACEMESH_CONTOURS, 
                                                  landmark_drawing_spec=None, 
                                                #   connection_drawing_spec=mp_styles.get_default_face_mesh_contours_style()
                                                  )
                        
                        mp_drawing.draw_landmarks(image=frame, 
                                                  landmark_list=landmarks, 
                                                  connections=mp_mesh.FACEMESH_IRISES, 
                                                  landmark_drawing_spec=None, 
                                                #   connection_drawing_spec=mp_styles.get_default_face_mesh_iris_style()
                                                  )
    - ESC 키를 누르면 프로그램이 종료되도록 설정한다.
      ```python
                if cv.waitKey(5) == 27:
                    break
      ```


  #### 결과 화면
  ![스크린샷 2025-04-15 212418](https://github.com/user-attachments/assets/ca1130fb-0538-42e1-9550-d8e63deb3cf5)





---
