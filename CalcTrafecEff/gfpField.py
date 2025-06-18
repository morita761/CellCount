import cv2
import numpy as np

src = cv2.imread("./oikawa/60_2'.tiff")

# resize
bsize = 640
basePixSize = bsize
height = src.shape[0]
width = src.shape[1]
largeSize = max(height, width)
resizeRate = basePixSize / largeSize
dst = cv2.resize(src, (int(width * resizeRate), int(height * resizeRate)),interpolation=cv2.INTER_CUBIC)
cv2.imshow("img_ori", dst)

# 白黒変換(gray化)
img_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
cv2.imshow("img_gray",img_gray)


threshold = 20
# 二値化(閾値100を超えた画素を255にする。)
ret, img_filter2 = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY)
cv2.imshow("two_img_filter",img_filter2)

contours, tmp = cv2.findContours(image=img_filter2, mode=cv2.RETR_TREE,method=cv2.CHAIN_APPROX_SIMPLE)
result = cv2.drawContours(image=dst, contours=contours,contourIdx=-1, color=(0, 0, 255),thickness=2, lineType=cv2.LINE_AA)
cv2.imshow('Result', result)

# 画面占有率
whole_area = img_filter2.size
# 黒領域の画素数
white_area = cv2.countNonZero(img_filter2)
# コンフルエンシーを表示
ratio = float(white_area / whole_area * 100)
print('cell confluency = ' + str( round(ratio, 2) ) + ' %')

cv2.waitKey(0)
cv2.destroyAllWindows()
