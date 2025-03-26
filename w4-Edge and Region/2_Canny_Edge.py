import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('soccer.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)      # 이미지를 그레이스케일로 변환

canny = cv.Canny(gray, 100, 200)

lines = cv.HoughLinesP(canny, 1, np.pi/180, 50, minLineLength=10, maxLineGap=1)

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2, cv.LINE_AA)

plt.figure(figsize=(15, 10))

plt.subplot(1, 2, 1)
plt.imshow(gray, cmap='gray')
plt.title('Original')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.title('Hough Lines')
plt.axis('off')

plt.show()
