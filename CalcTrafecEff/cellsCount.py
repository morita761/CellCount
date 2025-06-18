import cv2
import numpy as np
import sys

# パラメータ読み込み関数
def load_config(config_path='config.txt'):
    config = {
        'gaussian_kernel_size': 25,
        'gaussian_sigma': 2,
        'median_blur_ksize': 25,
        'threshold': 200,
        'area_threshold': 400,
        'resize_base': 640,
    }
    try:
        with open(config_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, val = line.strip().split('=')
                    if key in config:
                        config[key] = int(val)
    except FileNotFoundError:
        print("config.txt not found. Using default parameters.")
    return config

def findContours(src_gray, ori, config):
    gk = config['gaussian_kernel_size']
    sigma = config['gaussian_sigma']
    mk = config['median_blur_ksize']
    threshold = config['threshold']
    area_thresh = config['area_threshold']

    # 1. Gaussian blur
    img_gau = cv2.GaussianBlur(src_gray, (gk, gk), sigma)
    cv2.imshow("1. Gaussian Blur", img_gau)

    # 2. Median filter
    img_med = cv2.medianBlur(img_gau, mk)
    cv2.imshow("2. Median Blur", img_med)

    # 3. Thresholding
    _, img_bin = cv2.threshold(img_med, threshold, 255, cv2.THRESH_BINARY)
    cv2.imshow("3. Binary Threshold", img_bin)

    # 4. Contour detection
    contours, _ = cv2.findContours(img_bin, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours_large = [c for c in contours if cv2.contourArea(c) >= area_thresh]
    small_area_sum = sum(cv2.contourArea(c) for c in contours if cv2.contourArea(c) < area_thresh)

    # 5. Draw contours
    result = cv2.drawContours(ori.copy(), contours_large, -1, (0, 0, 255), 2)
    cv2.imshow('4. Contour Result', result)

    # 面積計算
    whole_area = img_bin.size
    white_area = cv2.countNonZero(img_bin)
    black_area = whole_area - white_area - int(small_area_sum)

    print(f"Black area (cell area estimate): {black_area}")
    ratio = black_area / whole_area * 100
    print(f"cell confluency = {round(ratio, 2)} %")

def setting(src):
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    cv2.imshow("0. Grayscale", gray)

    adaptive = cv2.adaptiveThreshold(gray, 255,
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY,
                                     11, 2)
    cv2.imshow("0.5 Adaptive Threshold", adaptive)
    return adaptive


def resize(src, base_size):
    h, w = src.shape[:2]
    rate = base_size / max(h, w)
    return cv2.resize(src, (int(w * rate), int(h * rate)), interpolation=cv2.INTER_CUBIC)

if __name__ == '__main__':
    config = load_config()

    if len(sys.argv) < 2:
        print("Note: using default image path './seq86095.tif'")
        img_path = "./seq86095.tif"
    else:
        img_path = sys.argv[1]

    src = cv2.imread(img_path)
    ori = resize(src, config['resize_base'])

    cv2.imshow("Original Image", ori)
    gray = setting(ori)
    findContours(gray, ori, config)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
