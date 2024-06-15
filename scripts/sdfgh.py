# coding=utf-8
import cv2
import numpy as np

img = cv2.imread("img_1.png", 0)

gray_lap = cv2.Laplacian(img, cv2.CV_32F, ksize=5)
dst = cv2.convertScaleAbs(gray_lap)  # 转回uint8
dst = cv2.GaussianBlur(dst, (3, 3), 3)

img = cv2.GaussianBlur(img, (3, 3), 0)
canny = cv2.Canny(img, 50, 150)


imgSobel = cv2.bitwise_or(canny, dst)
cv2.imshow('Sobel img', imgSobel)

cv2.imshow('img', canny)


cv2.waitKey(0)
cv2.destroyAllWindows()