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

# print(photo_list)
# print(photo_num)


for p in range(len(photo_list) - 1):

    # print(photo_list[p][0])
    name = 'frames/' + str(photo_list[p][0])
    name2 = 'frames/' + str(photo_list[p + 1][0])

    img = cv2.imread(name)
    img2 = cv2.imread(name2)
    peopleSize = np.zeros((6, 2))
    peopleSize2 = np.zeros((6, 2))
    peopleCoord = np.zeros((6, 2))
    peopleCoord2 = np.zeros((6, 2))
    peopleCount = []

    # if photo_num[p] == 0:
    #     for i in range(int(list_of_lists[photo_num[p] + 1][0])):
    #         people[i][0] = float(list_of_lists[photo_num[p] + 2 + i][2])
    #         people[i][1] = float(list_of_lists[photo_num[p] + 2 + i][3])
    #
    #         print('cos')
    #
    # # print(name)
    # else :

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

        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
    tmp = np.zeros((1, 2))
    for i in range(int(list_of_lists[photo_num[p + 1] + 1][0])):

        x1 = float(list_of_lists[photo_num[p + 1] + 2 + i][0])
        y1 = float(list_of_lists[photo_num[p + 1] + 2 + i][1])
        x2 = float(list_of_lists[photo_num[p + 1] + 2 + i][0]) + float(list_of_lists[photo_num[p + 1] + 2 + i][2])
        y2 = float(list_of_lists[photo_num[p + 1] + 2 + i][1]) + float(list_of_lists[photo_num[p + 1] + 2 + i][3])


        peopleCoord2[i][0] = float(list_of_lists[photo_num[p + 1] + 2 + i][0])
        peopleCoord2[i][1] = float(list_of_lists[photo_num[p + 1] + 2 + i][1])
        peopleSize2[i][0] = float(list_of_lists[photo_num[p + 1] + 2 + i][2])
        peopleSize2[i][1] = float(list_of_lists[photo_num[p + 1] + 2 + i][3])
        personnumber = -1
        for j in range(int(list_of_lists[photo_num[p] + 1][0])):
            first_prob = np.sum(1 - np.abs(np.subtract(peopleSize[j], peopleSize2[i])) / peopleSize2[i])/2
            # print(first_prob)
            tmpSize = np.sum(tmp)/2
            # print(tmpSize)
            if first_prob>tmpSize and first_prob>0.5:
                tmp = 1 - np.abs(np.subtract(peopleSize[j], peopleSize2[i])) / peopleSize2[i]
                personnumber = j
                # print(tmp)


        print(tmp)
        print(personnumber)
        cv2.rectangle(img2, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)

    # print(np.amax(1 - np.abs(np.subtract(peopleSize, peopleSize2[0])) / peopleSize2[0], axis=0))
    # print(np.abs(np.subtract(peopleCoord, peopleCoord2[0])))
    print(peopleCount)
    # print(np.where(1 - np.abs(np.subtract(peopleSize, peopleSize2[0])) / peopleSize2[0] == np.amax(1 - np.abs(np.subtract(peopleSize, peopleSize2[0])) / peopleSize2[0], axis=0)))
    # for p in people2:
    #     diff1tmp=100.
    #     diff2tmp=100.
    #     if p[0]!=0.0:
    #         for o in people:
    #             if o[0]!=0.0:
    #                 diff1 = np.abs((p[0]-o[0]))
    #                 diff2 = np.abs((p[1] - o[1]))
    #                 if diff1 < diff1tmp and diff2 < diff2tmp:
    #                     diff1tmp = diff1
    #                     diff2tmp = diff2
    # print(people)
    # print(people2)
    cv2.imshow('frame', img)
    cv2.imshow('frame2', img2)
    cv2.waitKey(0)