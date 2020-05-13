import cv2
import numpy as np
from pathlib import Path
from PIL import Image

img = cv2.imread("file3.jpg",cv2.IMREAD_GRAYSCALE)
_, threshold = cv2.threshold(img, 245, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
	approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
	cv2.drawContours(img, [cnt], 0, (0), 5)
cv2.imwrite("file4.jpg",img)