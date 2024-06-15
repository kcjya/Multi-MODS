import cv2 as cv
import numpy as np


def line_detection(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)#转化为灰度

    gray_lap = cv.Laplacian(gray, cv.CV_64F, ksize=7)
    dst = cv.convertScaleAbs(gray_lap)  # 转回uint8
    edges = cv.Canny(gray, 50, 150, apertureSize=5)#求取边缘 窗口大小apertureSize=3
    cv.imshow("ss22",edges)
    edges = cv.bitwise_and(edges, dst)

    lines = cv.HoughLines(edges, 1, np.pi/180, 125)#np.pi/180每次偏转1度
    cv.imshow("ss",edges)
    try:
        for line in lines:
            rho, theta = line[0]
            if rho<-120:
                continue
            print(line)
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0+1000*(-b))
            y1 = int(y0+1000*(a))
            x2 = int(x0-1000*(-b))
            y2 = int(y0-1000*(a))
            cv.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    except:pass
    cv.imshow("image-lines", image)


src = cv.imread("img_1.png")
cv.namedWindow("input image", cv.WINDOW_AUTOSIZE)
cv.imshow("input image", src)
line_detection(src)
cv.waitKey(0)

cv.destroyAllWindows()
