import numpy as np

import cv2

img = cv2.imread('frames/c6s1_000451.jpg')
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

for p in range(len(photo_list) - 1):

    name = 'frames/' + str(photo_list[p][0])
    name2 = 'frames/' + str(photo_list[p + 1][0])

    img = cv2.imread(name)
    img2 = cv2.imread(name2)
    peopleSize = np.zeros((6, 2))
    peopleSize2 = np.zeros((6, 2))
    peopleCoord = np.zeros((6, 2))
    peopleCoord2 = np.zeros((6, 2))
    peopleCount = []
    found_people = 0
    num_o_people = 0
    threshhold = 0.8

    for i in range(int(list_of_lists[photo_num[p] + 1][0])):
        x1 = float(list_of_lists[photo_num[p] + 2 + i][0])
        y1 = float(list_of_lists[photo_num[p] + 2 + i][1])
        x2 = float(list_of_lists[photo_num[p] + 2 + i][0]) + float(list_of_lists[photo_num[p] + 2 + i][2])
        y2 = float(list_of_lists[photo_num[p] + 2 + i][1]) + float(list_of_lists[photo_num[p] + 2 + i][3])

        peopleCoord[i][0] = float(list_of_lists[photo_num[p] + 2 + i][0])
        peopleCoord[i][1] = float(list_of_lists[photo_num[p] + 2 + i][1])
        peopleSize[i][0] = float(list_of_lists[photo_num[p] + 2 + i][2])
        peopleSize[i][1] = float(list_of_lists[photo_num[p] + 2 + i][3])
        peopleCount.append(i)

        # cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
    tmp = 0.0
    for i in range(int(list_of_lists[photo_num[p + 1] + 1][0])):

        x1 = float(list_of_lists[photo_num[p + 1] + 2 + i][0])
        y1 = float(list_of_lists[photo_num[p + 1] + 2 + i][1])
        x2 = float(list_of_lists[photo_num[p + 1] + 2 + i][0]) + float(list_of_lists[photo_num[p + 1] + 2 + i][2])
        y2 = float(list_of_lists[photo_num[p + 1] + 2 + i][1]) + float(list_of_lists[photo_num[p + 1] + 2 + i][3])

        peopleCoord2[i][0] = float(list_of_lists[photo_num[p + 1] + 2 + i][0])
        peopleCoord2[i][1] = float(list_of_lists[photo_num[p + 1] + 2 + i][1])
        peopleSize2[i][0] = float(list_of_lists[photo_num[p + 1] + 2 + i][2])
        peopleSize2[i][1] = float(list_of_lists[photo_num[p + 1] + 2 + i][3])
        num_o_people += 1
        personnumber = -1
        for j in range(int(list_of_lists[photo_num[p] + 1][0])):
            threshhold_local = threshhold
            first_prob = np.sum(1 - np.abs(np.subtract(peopleSize[j], peopleSize2[i])) / peopleSize2[i]) / 2
            sec_prob = np.sum(1 - np.abs(np.subtract(peopleCoord[j], peopleCoord2[i]))/[img.shape[1], img.shape[0]]) / 2

            color1 = img[int(peopleCoord[j][1]):int(peopleCoord[j][1] + peopleSize[j][1]),
                     int(peopleCoord[j][0]):int(peopleCoord[j][0] + peopleSize[j][0])]
            color2 = img2[int(y1):int(y2),
                     int(x1):int(x2)]
            center1x=color1.shape[0]/2
            center1y = color1.shape[1]/2
            color1comp = color1[int(center1x-10):int(center1x+10), int(center1y-10):int(center1y+10)]
            center2x=color2.shape[0]/2
            center2y = color2.shape[1]/2
            color2comp = color2[int(center2x-10):int(center2x+10), int(center2y-10):int(center2y+10)]

            third_prob = np.sum(1 - np.abs(np.mean(color2comp)- np.mean(color1comp)) / 256)

            full_prob = 0.4 * first_prob + 0.1 * sec_prob +0.5*third_prob
            print("full_prob: ", full_prob)
            print("contains")
            print(first_prob)
            print(sec_prob)
            print(third_prob)
            print("end of prob")
            if full_prob > tmp and full_prob > threshhold_local:
                tmp = full_prob
                personnumber = j

        print("Person Number: ", personnumber)
        if personnumber != -1:
            found_people+=1
    print("Number of found people ", found_people)
    print("% of found people ", found_people/np.min([num_o_people, len(peopleCount)]))
    print("peopleCount: ", peopleCount)

    cv2.imshow('frame', img)
    cv2.imshow('frame2', img2)
    cv2.waitKey(0)
    print("*******************NEW____PHOTO*****************")
