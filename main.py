import numpy as np

from PIL import Image

import cv2

img = cv2.imread('frames/c6s1_000451.jpg')
# f = open('bboxes.txt')
# content = f.read()
# print(content)
a_file = open("bboxes.txt", "r")

list_of_lists = []
for line in a_file:
    stripped_line = line.strip()
    line_list = stripped_line.split()
    list_of_lists.append(line_list)

a_file.close()

x1 = float(list_of_lists[2][0]) + float(list_of_lists[2][2])
y1 = float(list_of_lists[2][1])
x2 = float(list_of_lists[2][0])
y2 = float(list_of_lists[2][1])+ float(list_of_lists[2][3])
print((x1, y1))
print((x2, y2))
cv2.line(img,(int(float(list_of_lists[2][0])),int(float(list_of_lists[2][1]))),(int(float(list_of_lists[2][0]))+5,int(float(list_of_lists[2][1]))),(255,0,0),5)
cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
cv2.imshow('frame', img)
cv2.waitKey(0)
