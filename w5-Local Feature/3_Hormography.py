import cv2 as cv
import numpy as np
import time
from matplotlib import pyplot as plt

img1 = cv.imread('img1.jpg')
gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
img2 = cv.imread('img2.jpg')
gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

sift = cv.SIFT_create()
kp1, des1 = sift.detectAndCompute(gray1, None)
kp2, des2 = sift.detectAndCompute(gray2, None)

T=0.7
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann_matcher = cv.FlannBasedMatcher(index_params, search_params)    # FlannBasedMatcher() 사용
flann_knn_match = flann_matcher.knnMatch(des1, des2, k=2)

flann_good_match = []
for nearest1, nearest2 in flann_knn_match:
    if(nearest1.distance/nearest2.distance)<T:
        flann_good_match.append(nearest1)
        
img_match = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype=np.uint8)
flann_img = cv.drawMatches(img1, kp1, img2, kp2, flann_good_match, img_match, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

points1 = np.float32([kp1[m.queryIdx].pt for m in flann_good_match])
points2 = np.float32([kp2[m.trainIdx].pt for m in flann_good_match])

H,_= cv.findHomography(points1, points2, cv.RANSAC)

h1, w1 = img1.shape[:2]
corners1 = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]]).reshape(-1, 1, 2)
transformed_corners1 = cv.perspectiveTransform(corners1, H)


h2, w2 = img2.shape[:2]
corners2 = np.float32([[0, 0], [w2, 0], [w2, h2], [0, h2]]).reshape(-1, 1, 2)

all_corners = np.concatenate((transformed_corners1, corners2), axis=0)
[x_min, y_min] = np.int32(all_corners.min(axis=0).ravel() - 10)
[x_max, y_max] = np.int32(all_corners.max(axis=0).ravel() + 10)

new_width = x_max - x_min
new_height = y_max - y_min

translation_matrix = np.array([[1, 0, -x_min], [0, 1, -y_min], [0, 0, 1]]) 
H_translated = translation_matrix @ H

cv.imshow('Warped Image', img1_aligned)

img2_translated = np.zeros((new_height, new_width, 3), dtype=np.uint8)
img2_translated[-y_min:h2 - y_min, -x_min:w2 - x_min] = img2

blend = cv.addWeighted(img1_aligned, 0.5, img2_translated, 0.5, 0)
cv.imshow('Blended Image', blend)

cv.destroyAllWindows()

plt.figure(figsize=(18, 8))

# plt.subplot(1, 4, 1)
# plt.imshow(cv.cvtColor(img1, cv.COLOR_BGR2RGB))
# plt.title('img1.jpg')
# plt.axis('off')

# plt.subplot(1, 4, 2)
# plt.imshow(cv.cvtColor(img2, cv.COLOR_BGR2RGB))
# plt.title('img2.jpg')
# plt.axis('off')

# plt.subplot(1, 4, 3)
# plt.imshow(cv.cvtColor(bf_img, cv.COLOR_BGR2RGB))
# plt.title('BFMatcher')
# plt.axis('off')

# plt.subplot(1, 4, 4)
# plt.imshow(cv.cvtColor(blend, cv.COLOR_BGR2RGB))
# plt.title('Alignment')
# plt.axis('off')

plt.subplot(1, 2, 1)
plt.imshow(cv.cvtColor(flann_img, cv.COLOR_BGR2RGB))
plt.title('BFMatcher')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(cv.cvtColor(blend, cv.COLOR_BGR2RGB))
plt.title('Alignment')
plt.axis('off')

plt.show()
