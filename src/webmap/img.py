import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import numpy as np

map = mpimg.imread("../resources/images/map-2.png") # 读取和代码处于同一目录下的 lena.png

plt.imshow(map)
plt.axis('off')
plt.show()