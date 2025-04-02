import cv2 as cv
import numpy as np
import time
from matplotlib import pyplot as plt

img1 = cv.imread('mot_color70.jpg')[190:350, 440:560]
gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
img2 = cv.imread('mot_color83.jpg')
gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

sift = cv.SIFT_create()
kp1, des1 = sift.detectAndCompute(gray1, None)
kp2, des2 = sift.detectAndCompute(gray2, None)

print('특징점 개수: ', len(kp1), len(kp2))

start = time.time()
bf_matcher = cv.BFMatcher(cv.NORM_L2, crossCheck=True)
bf_match = bf_matcher.match(des1, des2)

FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann_matcher = cv.FlannBasedMatcher(index_params, search_params)    # FlannBasedMatcher() 사용
flann_knn_match = flann_matcher.knnMatch(des1, des2, k=2)


T=0.7
bf_good_match = []
for match in bf_match:
    bf_good_match.append(match)
print('BF 매칭에 걸린 시간: ', time.time()-start)

falnn_good_match = []
for nearest1, nearest2 in flann_knn_match:
    if(nearest1.distance/nearest2.distance)<T:
        falnn_good_match.append(nearest1)
print('Flann 매칭에 걸린 시간: ', time.time()-start)


img_match = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype=np.uint8)
bf_img = cv.drawMatches(img1, kp1, img2, kp2, bf_good_match, img_match, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
flann_img = cv.drawMatches(img1, kp1, img2, kp2, falnn_good_match, img_match, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

cv.imshow('Good Matches', img_match)

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(cv.cvtColor(bf_img, cv.COLOR_BGR2RGB))
plt.title('BFMatcher')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(cv.cvtColor(flann_img, cv.COLOR_BGR2RGB))
plt.title('FlannBasedMatcher')
plt.axis('off')

plt.show()
