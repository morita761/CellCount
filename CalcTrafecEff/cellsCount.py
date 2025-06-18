import cv2
import numpy as np
import sys

# python cellsCountCode.py 使用する画像のPATH(例：./seq86095.tif ) 細胞と判別する閾値(default: 200)
# 閾値は0~255
if len(sys.argv) < 2:
    print("Note: using default imgage now")
    src = cv2.imread("./seq86095.tif")

if len(sys.argv) >= 2:
    img_path = sys.argv[1]
    src = cv2.imread(img_path)

if len(sys.argv) >= 3:
    threshold = int(sys.argv[2])
else:
    threshold = 200



def findContours(src, ori):
    img_gau = cv2.GaussianBlur(src, (25,25), 2)
    # cv2.imshow("img_gau", img_gau)

    img_med2 = cv2.medianBlur(img_gau, 25)
    # cv2.imshow("img_medd", img_med2)

    # threshold = int(img[2])

    # 二値化(閾値100を超えた画素を255にする。)
    ret, img_filter2 = cv2.threshold(img_med2, threshold, 255, cv2.THRESH_BINARY)
    # cv2.imshow("two_img_filter",img_filter2)

    # blend = cv2.addWeighted(src1=ori,alpha=0.5,src2=img_filter2,beta=0.7,gamma=50)
    # cv2.imshow("blend",blend)

    sikiiti = 400

    contours, hierarchy = cv2.findContours(img_filter2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours_by__area = list(filter(lambda x: cv2.contourArea(x) >= sikiiti, contours))

    sum = 0
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        if(area < sikiiti):
            # print(f"{i}, area{i}: {area}")
            sum += area

    result = cv2.drawContours(image=ori, contours=contours_by__area, contourIdx=-1, color=(0, 0, 255),thickness=2, lineType=cv2.LINE_AA)
    cv2.imshow('Result', result)

    # 画面占有率
    whole_area = img_filter2.size
    # 黒領域の画素数
    white_area = cv2.countNonZero(img_filter2)
    black_area = whole_area - white_area - int(sum)
    print(black_area)

    # コンフルエンシーを表示
    ratio = float( black_area / whole_area * 100)
    print('cell confluency = ' + str( round(ratio, 2) ) + ' %')

def setting(src):
    img_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    th2 = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    cv2.imshow("img_th", th2)
    return th2

def resize(src, bsize):
    basePixSize = bsize
    height = src.shape[0]
    width = src.shape[1]
    largeSize = max(height, width)
    resizeRate = basePixSize / largeSize
    dst = cv2.resize(src, (int(width * resizeRate), int(height * resizeRate)),interpolation=cv2.INTER_CUBIC)
    return dst

if __name__ == '__main__':
    # src = cv2.imread("./source/seq86097.tif")
    ori = resize(src, 640) 
    cv2.imshow("Original", ori)
    dst = setting(ori)
    dst = findContours(dst, ori)
    # dst = findContours(dst, ori)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()
