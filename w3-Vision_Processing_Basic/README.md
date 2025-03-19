### 01 이진화 및 히스토그램 구하기
---

- 주어진 이미지를 불러와서 다음을 수행
  1. 이미지를 그레이스케일로 변환
  2. 특정 임계값을 설정하여 이진화
  3. 이진화된 이미지의 히스토그램을 계산하고 시각화
 
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
      gray_hist = cv.calcHist([gray], [0], None, [256], [0, 256])
      plt.plot(gray_hist, color='r', linewidth=1)
      plt.show()
    ```

  #### 결과화면
- 이진화 이미지
![image](https://github.com/user-attachments/assets/cf72fee6-3749-46d0-8a36-53ec58706bb5)

- 히스토그램
  ![image](https://github.com/user-attachments/assets/7a8b23b6-4961-494f-a498-028d29c43c6f)

  



---
