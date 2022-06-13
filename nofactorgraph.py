import numpy as np

import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data_dir', type=str)
args = parser.parse_args()


box = args.data_dir+"bboxes.txt"
a_file = open(box, "r")

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
num_o_found = 1.0 #Value used to change threshold
for p in range(len(photo_list) - 1):

    name = args.data_dir+'frames/' + str(photo_list[p][0])
    name2 = args.data_dir+'frames/' + str(photo_list[p + 1][0])

    img = cv2.imread(name)
    img2 = cv2.imread(name2)
    peopleSize = np.zeros((6, 2)) #Matrix including sizes of bboxes in current photo
    peopleSize2 = np.zeros((6, 2)) #Matrix including sizes of bboxes in next photo
    peopleCoord = np.zeros((6, 2)) #Matrix including coordinates of bboxes in current photo
    peopleCoord2 = np.zeros((6, 2)) #Matrix including coordinates of bboxes in next photo
    peopleCount = [] #List including number of people found in current photo
    found_people = 0 #Number of people found between 2 photos
    num_o_people = 0 #Number of people in next photo
    threshold = 0.8 #Base value of threshold
    people = [] #List containing indexes of people found between 2 photos

    for i in range(int(list_of_lists[photo_num[p] + 1][0])):
        peopleCoord[i][0] = float(list_of_lists[photo_num[p] + 2 + i][0])
        peopleCoord[i][1] = float(list_of_lists[photo_num[p] + 2 + i][1])
        peopleSize[i][0] = float(list_of_lists[photo_num[p] + 2 + i][2])
        peopleSize[i][1] = float(list_of_lists[photo_num[p] + 2 + i][3])
        peopleCount.append(i)

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
        #Adapting threshold
        threshold_local = threshold * num_o_found
        for j in range(int(list_of_lists[photo_num[p] + 1][0])):
            ### Color calculation ###
            color1 = img[int(peopleCoord[j][1]):int(peopleCoord[j][1] + peopleSize[j][1]),
                     int(peopleCoord[j][0]):int(peopleCoord[j][0] + peopleSize[j][0])]
            color2 = img2[int(y1):int(y2),
                     int(x1):int(x2)]
            center1x = color1.shape[0] / 2
            center1y = color1.shape[1] / 2
            color1comp = color1[int(center1x - 10):int(center1x + 10), int(center1y - 10):int(center1y + 10)]
            center2x = color2.shape[0] / 2
            center2y = color2.shape[1] / 2
            color2comp = color2[int(center2x - 10):int(center2x + 10), int(center2y - 10):int(center2y + 10)]
            ###########################

            #Size difference of bboxes
            first_prob = np.sum(1 - np.abs(np.subtract(peopleSize[j], peopleSize2[i])) / peopleSize2[i]) / 2
            #Distance between two bboxes
            sec_prob = np.sum(
                1 - np.abs(np.subtract(peopleCoord[j], peopleCoord2[i])) / [img.shape[1], img.shape[0]]) / 2
            #Difference between mean colors in the centres of bboxes
            third_prob = np.sum(1 - np.abs(np.mean(color2comp) - np.mean(color1comp)) / 255)

            #Full probability including weights
            full_prob = 0.4 * first_prob + 0.1 * sec_prob + 0.5 * third_prob
            # probs.append(full_prob)
            if full_prob > tmp and full_prob > threshold_local:
                tmp = full_prob
                personnumber = j
        people.append(personnumber)
        if personnumber != -1:
            found_people += 1
    num_o_found = found_people / np.min([num_o_people, len(peopleCount)])
    if num_o_found < 0.5:
        num_o_found = 0.5  # minimum size for treshhold
    print(*people)
    people = []

