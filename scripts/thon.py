import matplotlib.pyplot as plt
import cv2
import numpy as np

# 读取RGB图像
image = cv2.imread('img.png')

# 将图像从BGR颜色空间转换为RGB颜色空间
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 提取每个通道的像素值

red_channel = image[:, :, 0].flatten()
green_channel = image[:, :, 1].flatten()
blue_channel = image[:, :, 2].flatten()
r = cv2.calcHist([red_channel], [0], None, [256], [0, 256])
g = cv2.calcHist([green_channel], [0], None, [256], [0, 256])
b = cv2.calcHist([blue_channel], [0], None, [256], [0, 256])
# 创建x轴的像素位置
x = np.arange(256)

# 创建一个新的图形窗口
plt.figure(figsize=(8, 6))

# 绘制红色通道曲线
plt.plot(x, np.ravel(r), color='red', label='Red Channel')

# 绘制绿色通道曲线
plt.plot(x, np.ravel(g), color='green', label='Green Channel')

# 绘制蓝色通道曲线
plt.plot(x, np.ravel(b), color='blue', label='Blue Channel')

# 设置图例位置和边框
plt.legend(loc='upper right', frameon=False)
plt.xlabel('Pixel Intensity')
plt.ylabel('Value')
# 设置图形的边距
plt.tight_layout(pad=10)

# 显示图像
plt.show()