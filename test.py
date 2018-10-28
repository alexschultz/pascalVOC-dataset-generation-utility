import cv2
import os
import numpy as np

OUTPUT_PATH = './generated/'

testImg = cv2.imread('./generated/generated-0.jpg', cv2.IMREAD_COLOR)
roi = testImg[233:324, 557:649]
cv2.imshow('Test Out', roi)
cv2.waitKey(0)
cv2.destroyAllWindows()
