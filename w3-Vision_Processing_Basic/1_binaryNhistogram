import cv2 as cv
import sys
from matplotlib import pyplot as plt

img = cv.imread('soccer.jpg', cv.IMREAD_GRAYSCALE)
gray = cv.cvtColor(img, cv.COLOR_BAYER_BG2BGR)

if img is None:
    sys.exit('파일을 찾을 수 없습니다.')
    
t, bin_img = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
cv.imshow('Channel binarization', bin_img)

# hist = cv.calcHist([img], [0], None, [256], [0, 256])
# plt.plot(hist, color='r', linewidth=1)
# plt.show()

gray_hist = cv.calcHist([gray], [0], None, [256], [0, 256])
plt.plot(gray_hist, color='r', linewidth=1)
plt.show()

cv.waitKey()
cv.destroyAllWindows()
