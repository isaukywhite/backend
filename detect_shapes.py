import cv2
import numpy as np
from pathlib import Path
from PIL import Image

def ultimoarquivo():
    data_criacao = lambda f: f.stat().st_ctime
    data_modificacao = lambda f: f.stat().st_mtime

    directory = Path('C:/Users/Isac/Desktop/police/Instinct_AngleView_Pro_3.0.3.7')
    files = directory.glob('*.jpg')
    sorted_files = sorted(files, key=data_modificacao, reverse=True)
    print(sorted_files[0])
    return(sorted_files[0])

img = cv2.imread(str(ultimoarquivo()), cv2.IMREAD_GRAYSCALE)

maxX = 633
minX = 549
maxY = 465
minY = 381

size = 840, 840


crop_img = img[minY:maxY, minX:maxX]
img = crop_img

img2 = cv2.resize(img, size, fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
img = img2

cv2.imwrite("file.jpg", img)

_, threshold = cv2.threshold(img, 245, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
	approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
	cv2.drawContours(img, [cnt], 0, (0), 5)

cv2.imwrite("file2.jpg", img2)

# cv2.imshow("img", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
