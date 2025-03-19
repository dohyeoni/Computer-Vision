import cv2 as cv
import sys
from matplotlib import pyplot as plt
import numpy as np

img = cv.imread('JohnHancocksSignature.png', cv.IMREAD_UNCHANGED)
image = img[img.shape[0]//2:img.shape[0], 0:img.shape[0]//2+1]

if img is None:
    sys.exit('파일을 찾을 수 없습니다.')
    
kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
print(kernel)

b_dilation = cv.morphologyEx(image, cv.MORPH_DILATE, kernel)  # 팽창
b_erosion = cv.morphologyEx(image, cv.MORPH_ERODE, kernel)    # 침식
b_open = cv.morphologyEx(image, cv.MORPH_OPEN, kernel)        # 열림
b_close = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)      # 닫힘 

result = np.hstack([image, b_dilation, b_erosion, b_open, b_close])

plt.imshow(result)
plt.show()
