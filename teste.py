import cv2, numpy as np, argparse

gray = cv2.imread("file.jpg", cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
cv2.imwrite("file3.jpg", edges)
lines = cv2.HoughLines(edges, 1, np.pi / 180, 20)
left = [0, 0]
right = [0, 0]
up = [0, 0]
down = [0, 0]
for object in lines:
    theta = object[0][1]
    rho = object[0][0]
    if ((np.round(theta, 2)) >= 1.0 and (np.round(theta, 2)) <= 1.1) or ((np.round(theta,2)) >= 2.0 and (np.round(theta,2)) <= 2.1):
        if (rho >= 20 and rho <= 30):
            left[0] += 1
        elif (rho >= 60 and rho <= 65):
            left[1] += 1
        elif (rho >= -73 and rho <= -57):
            right[0] += 1
        elif (rho >= 148 and rho <= 176):
            right[1] += 1
    elif ((np.round(theta, 2)) >= 0.4 and (np.round(theta, 2)) <= 0.6) or ((np.round(theta, 2)) >= 2.6 and (np.round(theta,2))<= 2.7):
        if (rho >= -63 and rho <= -15):
            up[0] += 1
        elif (rho >= 67 and rho <= 74):
            down[1] += 1
            up[1] += 1
        elif (rho >= 160 and rho <= 171):
            down[0] += 1

if left[0] >= 1 and left[1] >= 1:
    print("left")
elif right[0] >= 1 and right[1] >= 1:
    print("right")
elif up[0] >= 1 and up[1] >= 1:
    print("up")
elif down[0] >= 1 and down[1] >= 1:
    print("down")

print(up, down, left, right)
