## 01 이진화 및 히스토그램 구하기


- 주어진 이미지를 불러와서 다음을 수행
  1. 이미지를 그레이스케일로 변환
  2. 특정 임계값을 설정하여 이진화
  3. 이진화된 이미지의 히스토그램을 계산하고 시각화

  #### 요구사항
  - cv.imread() 사용해 이미지 불러오기
    ```python
      img = cv.imread('soccer.jpg', cv.IMREAD_GRAYSCALE)
    ```
  - cv.cvtColor() 사용해 그레이스케일로 변환
    ```python
      gray = cv.cvtColor(img, cv.COLOR_BAYER_BG2BGR)
    ```
  - cv.threshold() 사용해 이진화
    ```python
      t, bin_img = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
    ```
  - cv.calcHist() 사용해 히스토그램 계산 + matplotlib로 시각화
    ```python
      # Grayscale
      gray_hist = cv.calcHist([gray], [0], None, [256], [0, 256])
      plt.plot(gray_hist, color='r', linewidth=1)
      plt.title('Grayscale Image Histogram')
      plt.show()
      
      # Binary Image
      bin_hist = cv.calcHist([bin_img], [0], None, [256], [0, 256])
      plt.plot(bin_hist, color='r', linewidth=1)
      plt.title('Binary Image Histogram')
      plt.show()
    ```

  #### 결과화면
  - 이진화 이미지
  ![image](https://github.com/user-attachments/assets/cf72fee6-3749-46d0-8a36-53ec58706bb5)

  - 히스토그램
 
    <table align="center">
      <tr>
        <td align="center">
            <img src="https://github.com/user-attachments/assets/c864347f-a269-4868-bd5a-96ca09fc4de8" alt="binary" width="300"><br>
            <b>Gray</b>
        </td>
        <td align="center">
            <img src="https://github.com/user-attachments/assets/674ed18b-81d2-4135-a03c-f42e90adf87f" alt="gray" width="300"><br>
            <b>Binary</b>
        </td>
      </tr>
    </table>
    
  



---


## 02 모폴로지 연산 적용하기

  - 주어진 이진화된 이미지에 대해 팽창(Dilation)침식(Erosion)열림(Open)닫힘(Close) 모폴로지 연산 적용

     #### 요구사항
      - cv.getStructuringElement() 사용해 사각형 커널(5x5) 만들기
        ```python
          kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
        ```
      - cv.morphologyEx() 사용해 각 모폴로지 연산 적용
        ```python
          b_dilation = cv.morphologyEx(image, cv.MORPH_DILATE, kernel)  # 팽창
          b_erosion = cv.morphologyEx(image, cv.MORPH_ERODE, kernel)    # 침식
          b_open = cv.morphologyEx(image, cv.MORPH_OPEN, kernel)        # 열림
          b_close = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)      # 닫힘 
        ```
     - 원본 이미지와 모폴로지 연산 결과를 한 화면에 출력
        ```python
          images = [image, b_dilation, b_erosion, b_open, b_close]
          titles = ['Original','Dilation', 'Erosion', 'Open', 'Close']

          # 서브플롯 생성 (1행 5열)
          fig, axes = plt.subplots(1, 5, figsize=(15, 5))

          for i, ax in enumerate(axes):
            ax.imshow(images[i], cmap='gray')
            ax.set_title(titles[i], fontsize=12)
            ax.axis('off')
        ```


    #### 결과 화면
      ![스크린샷 2025-03-24 234448](https://github.com/user-attachments/assets/9d7b46fa-2174-4d67-bda9-170646233ed7)




---


## 03 기하 연산 및 선형 보간 적용하기

  - 주어진 이미지를 다음과 같이 변환하기
    1. 이미지를 45도 회전
    2. 회전된 이미지를 1.5배 확대
    3. 회전 및 확대된 이미지에 선형 보간(Bilinear Interpolation)을적용하여부드럽게표현

     #### 요구사항
      - cv.getRotationMatrix2D()를 사용하여 회전 변환 행렬 생성
        ```python
          rotation = cv.getRotationMatrix2D(cp, 45, 1.5)      # 45도 회전, 1.5배 확대
        ```
      - cv.warpAffine()를 사용하여 이미지 회전 및 확대
      - cv.INTER_LINEAR을 사용하여 선형 보간 적용
        ```python
          rows, cols = img.shape[:2]  # (높이, 너비, 채널수) 중 높이와 너비만 가져옴
          dst = cv.warpAffine(img, rotation, (int(cols*1.5), int(rows*1.5)), flags=cv.INTER_LINEAR)
        ```
    - 원본 이미지와 회전 및 확대된 이미지를 한화면에 비교
        ```python
          result = np.hstack([img, dst_resize])
          cv.imshow('Result', result)
        ```


    #### 결과 화면
      ![image](https://github.com/user-attachments/assets/5611404c-e553-41a0-a8b4-0f083a21d5a7)


    
