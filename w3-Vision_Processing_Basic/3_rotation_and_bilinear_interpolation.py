import cv2 as cv
import numpy as np
import math
import matplotlib.pyplot as plt

img = cv.imread('mistyroad.jpg')

cp = (img.shape[1]/2, img.shape[0]/2)
rotation = cv.getRotationMatrix2D(cp, 45, 1.5)      # 45도 회전, 1.5배 확대

rows, cols = img.shape[:2]  # (높이, 너비, 채널수) 중 높이와 너비만 가져옴
dst = cv.warpAffine(img, rotation, (int(cols*1.5), int(rows*1.5)), flags=cv.INTER_LINEAR)
dst_resize = cv.resize(dst, (img.shape[1], img.shape[0]))

plt.figure(figsize=(10,5))

result = np.hstack([img, dst_resize])
cv.imshow('Result', result)
cv.waitKey()
cv.destroyAllWindows()
