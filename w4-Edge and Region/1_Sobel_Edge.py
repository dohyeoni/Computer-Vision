import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np

img = cv.imread('soccer.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)      # 이미지를 그레이스케일로 변환

grad_x = cv.Sobel(gray, cv.CV_64F, 1, 0, ksize=3)   # 소벨 연산자 적용
grad_y = cv.Sobel(gray, cv.CV_64F, 0, 1, ksize=3)

mag = cv.magnitude(grad_x, grad_y)

mag_img = cv.convertScaleAbs(mag)   

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.title('Original')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(mag_img, cmap='gray')
plt.title('Edge Magnitude')
plt.axis('off')

plt.show()
