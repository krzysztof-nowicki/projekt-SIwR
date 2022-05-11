import numpy as np


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
photo_list = []
photo_num = []
for i, data in enumerate(list_of_lists):
    if any("c6s1_" in s for s in data):
        photo_list.append(data)
        photo_num.append(i)

print(photo_list)
print(photo_num)
for p in range(len(photo_list)):
    # print(photo_list[p][0])
    name = 'frames/' + str(photo_list[p][0])
    print(name)
    img = cv2.imread(name)
    for i in range(int(list_of_lists[photo_num[p]+1][0])):
        x1 = float(list_of_lists[photo_num[p]+2+i][0])
        y1 = float(list_of_lists[photo_num[p]+2+i][1])
        x2 = float(list_of_lists[photo_num[p]+2+i][0]) + float(list_of_lists[photo_num[p]+2+i][2])
        y2 = float(list_of_lists[photo_num[p]+2+i][1]) + float(list_of_lists[photo_num[p]+2+i][3])

        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)

    cv2.imshow('frame', img)
    cv2.waitKey(0)


