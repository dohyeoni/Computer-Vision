## 목적
  - 학습용 가상 한국 번호판 이미지 생성기

## 필요한 환경
  - python
  - 필요한 라이브러리 설치
    ``` bash
      pip install tqdm pillow colorama
    ```
  - tqdm: 진행바 표시
  - PTL (Pillow): 이미지 생성 및 편집
  - urllib.equest: 배경 이미지 다운로드

## 파일 설명
  - ```generate_img.py```: 생성한 이미지를 차량 이미지에 부착한 결과 사진을 저장
  - ```create_plate.py```: 랜덤 번호판 생성
  - 사용한 fonts
      - ```Hangil.ttf```: 한글용 글씨체
      - ```NotoSansKR-Medium.ttf```: 숫자용 글씨체

## 실행 방법
### create_plate.py
  **요약**
  
    1. 번호판 종류 결정
    2. 랜덤 글자 조합 (숫자 + 한글 + 숫자)
    3. 배경 이미지 열기
    4. 글자 위치에 텍스트 그리기
    5. 결과 이미지 저장

  **생성하는 번호판 종류**
  
    - 신형 8자리 번호판 (홀로그램)
    - 구형 8자리 번호판
    - 구형 7자리 번호판

  **한글 문자 셋 설정**
  
    - 차량별 번호판에 사용되는 한글 문자 분류
      - korean: 일반 차량 번호판에 사용할 한글 문자들
      - korean_taxi: 택시용 차량 번호판에 사용할 한글 문자들
      - korean_rent: 랜터카용 차량 번호판에 사용할 한글 문자들
      - korean_parcel: 택배 차량 번호판에 사용할 한글 문자들
   
  **배경 이미지**
  
    - ```images/src_plate_img/number_plate_new.png```: 신형 배경
    - ```images/src_plate_img/number_plate_old.png```: 구형 배경

   **문자열 조합 방법**
   
     - 앞자리 (숫자)
     - 중간자리 (한글 문자)
     - 뒷자리 (숫자)
     -> 세 부분을 이어 붙여 전체 번호판 문자열 생성
       
  => 이를 사용해 배경 이미지에 랜덤으로 생성한 번호(텍스트)를 그림


### generate_sysnthetic
  **전체 흐름 요약**
    1. plates/ 에서 번호판 이미지 불러오기
    2. labels/filtered_label/ 에서 JSON 파일 불러오기
    3. 각 차량에 대해
      - JSON 파일에서 차량과 번호판 바운딩박스를 읽기
    4. 차량 이미지 불러오기
    5. 불러온 이미지에 번호판 붙이기 (랜덤 선택 + 리사이즈)
    6. 결과 이미지 저장
      
  **메인 함수 ```genetate_synthetic_from_json()```**
    - 사용할 번호판 이미지 불러오기
      ``` python
        plate_files = [os.path.join(PLATE_IMAGE_DIR, f) for f in os.listdir(PLATE_IMAGE_DIR) if f.endswith(('.png', '.jpg'))]
      ```

    - 사용할 JSON 파일 목록 불러오기
    
      ``` python
        json_files = [f for f in os.listdir(JSON_LABEL_DIR) if f.endswith(".json")]
      ```

    - 차량 bbox + 번호판 bbox 추출
    
      ``` python
        car_pts = data['car']['bbox']
        plate_pts = data['plate']['bbox']
      ```
      - 좌표를 (x1, y1), (x2, y2) 형태로 정리
      - 좌표의 순서가 꼬이지 않게 정렬
    - 번호판 bbox 좌표 전환
      ``` python
        new_x1 = plate_x1 - cx1
        new_y1 = plate_y1 - cy1
        new_x2 = plate_x2 - cx1
        new_y2 = plate_y2 - cy1
      ```
      - 주어진 차량 이미지 안의 상대 위치로 번호판 좌표를 변환
    - 번호판 합성
      ``` python
        plate_img = random.choice(plate_files)
        plate_resized = cv2.resize(plate_img, (pw, ph))
        img[new_y1:new_y2, new_x1:new_x2] = plate_resized
      ```
      - 번호판 이미지 중 하나를 랜덤으로 선택
      - 번호판 bbox 크기에 맞게 리사이즈
      - 차량 이미지에 부착




