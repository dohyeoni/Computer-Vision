# mapping한 거 사진도 넣고
# 두 개 붙인 거 사진 넣고

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

bf_matcher = cv.BFMatcher(cv.NORM_L2, crossCheck=False)
bf_knn_match = bf_matcher.knnMatch(des1, des2, k=2)

T=0.7
bf_good_match = []
for nearest1, nearest2 in bf_knn_match:
    if(nearest1.distance/nearest2.distance)<T:
        bf_good_match.append(nearest1)
        
        
img_match = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype=np.uint8)
bf_img = cv.drawMatches(img1, kp1, img2, kp2, bf_good_match, img_match, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)


# 매칭된 특징점의 좌표 추출 
points1 = np.float32([kp1[m.queryIdx].pt for m in bf_good_match])    # queryIdx - img1의 매칭된 키포인트 인덱스
points2 = np.float32([kp2[m.trainIdx].pt for m in bf_good_match])    # trainIdx - img2의 매칭된 키포인트 인덱스

H,_= cv.findHomography(points1, points2, cv.RANSAC)     # 호모그래피 행렬 H(point1을 points2로 대응시킴): img1을 img2에 맞게 변형시킬 수 있는 변환 행렬 => 두 이미지에서 서로 대응하는 점의 좌표쌍을 뽑아냄 |RANSAC: outlier 제거거

h1, w1 = img1.shape[:2] # img1의 세로(h1), 가로(w1) 크기를 가져옴 -> 이미지의 모서리 좌표를 지정하기 위해 필요 
corners1 = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]]).reshape(-1, 1, 2)   #img1의 네 모서리를 H 행렬로 변형 
transformed_corners1 = cv.perspectiveTransform(corners1, H) # img1이 img2 시점으로 어떻게 왜곡되는지 계산 -> 정렬된 img1의 네 모서리 좌표가 반환됨 


h2, w2 = img2.shape[:2] # img2의 모서리도 정의 
corners2 = np.float32([[0, 0], [w2, 0], [w2, h2], [0, h2]]).reshape(-1, 1, 2)

# 두 이미지의 전체 범위를 감싸는 새로운 캔버스 크기 계산 
all_corners = np.concatenate((transformed_corners1, corners2), axis=0)  # 변환된 img1의 모서리 + img2의 모서리 => 전체를 감싸는 새로운 범위를 계산하기 위함 
[x_min, y_min] = np.int32(all_corners.min(axis=0).ravel() - 10)
[x_max, y_max] = np.int32(all_corners.max(axis=0).ravel() + 10)

# 평행이동 변환 행렬 적용 (좌표가 음수가 되지 않도록) 
new_width = x_max - x_min
new_height = y_max - y_min

translation_matrix = np.array([[1, 0, -x_min], [0, 1, -y_min], [0, 0, 1]]) 
H_translated = translation_matrix @ H   # 기존 호모그래피 H에 translation을 곱해서 -> 최종적으로 이미지 정합을 할 때 음수 좌표를 피하고 + 새로운 캔버스 상에서 정확히 맞춰주는 행렬

img1_aligned = cv.warpPerspective(img1, H_translated, (new_width, new_height))  # img1을 변환해서 새로운 좌표계에 맞게 정렬 | 변환된 H로 img1을 왜곡시키면서 새 캔버스에 맞게 투영 

cv.imshow('Warped Image', img1_aligned)

img2_translated = np.zeros((new_height, new_width, 3), dtype=np.uint8)      # img2도 정렬된 좌표계에 맞게 새로운 캔버스에 복사  (빈 배경 위에 img2를 지정 위치에 붙여넣는 느낌)
img2_translated[-y_min:h2 - y_min, -x_min:w2 - x_min] = img2

blend = cv.addWeighted(img1_aligned, 0.5, img2_translated, 0.5, 0)  # 두 이미지를 반투투명하게 합성해서 -> 겹쳐서 표시 
cv.imshow('Blended Image', blend)

cv.destroyAllWindows()

plt.figure(figsize=(18, 8))

plt.subplot(1, 4, 1)
plt.imshow(cv.cvtColor(img1, cv.COLOR_BGR2RGB))
plt.title('img1.jpg')
plt.axis('off')

plt.subplot(1, 4, 2)
plt.imshow(cv.cvtColor(img2, cv.COLOR_BGR2RGB))
plt.title('img2.jpg')
plt.axis('off')

plt.subplot(1, 4, 3)
plt.imshow(cv.cvtColor(blend, cv.COLOR_BGR2RGB))
plt.title('Alignment')
plt.axis('off')

plt.subplot(1, 4, 4)
plt.imshow(cv.cvtColor(bf_img, cv.COLOR_BGR2RGB))
plt.title('BFMatcher')
plt.axis('off')

plt.show()
