import matplotlib
import torch
import cv2


import matplotlib_inline
import numpy as np
import matplotlib
matplotlib.use('TkAgg')


model = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt')
# img = cv2.imread("tmpImg21.jpg")
# # cv2.imshow("o",img)
# # cv2.waitKey(0)
# result = model(img)
# result.show()
print(model)


  #  cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

