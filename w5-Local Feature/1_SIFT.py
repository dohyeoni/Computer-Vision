import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('mot_color70.jpg')          # 이미지 불러오기
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

sift = cv.SIFT_create()      # SIFT 객체 생성성
sift = cv.SIFT_create(nfeatures=100)  
kp, des = sift.detectAndCompute(gray, None)     # 특징점 검출

gray = cv.drawKeypoints(gray, kp, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)    # 특징점을 이미지에 시각화

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
