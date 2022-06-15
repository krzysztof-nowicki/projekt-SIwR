import numpy as np

import cv2
import argparse
from itertools import combinations
from pgmpy.models import FactorGraph

from pgmpy.factors.discrete import DiscreteFactor
from pgmpy.inference import BeliefPropagation

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
num_o_found = 1.0 
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

    names = []
    probs =[]

    for i in range(int(list_of_lists[photo_num[p] + 1][0])):
        peopleCoord[i][0] = float(list_of_lists[photo_num[p] + 2 + i][0])
        peopleCoord[i][1] = float(list_of_lists[photo_num[p] + 2 + i][1])
        peopleSize[i][0] = float(list_of_lists[photo_num[p] + 2 + i][2])
        peopleSize[i][1] = float(list_of_lists[photo_num[p] + 2 + i][3])
        peopleCount.append(i)

    G = FactorGraph()
    for i in range(int(list_of_lists[photo_num[p + 1] + 1][0])):
        probs = []
        name = "x"+str(i)
        names.append(name)
        G.add_node(name)
        phiname = "phi_"+name
        x1 = float(list_of_lists[photo_num[p + 1] + 2 + i][0])
        y1 = float(list_of_lists[photo_num[p + 1] + 2 + i][1])
        x2 = float(list_of_lists[photo_num[p + 1] + 2 + i][0]) + float(list_of_lists[photo_num[p + 1] + 2 + i][2])
        y2 = float(list_of_lists[photo_num[p + 1] + 2 + i][1]) + float(list_of_lists[photo_num[p + 1] + 2 + i][3])

        peopleCoord2[i][0] = float(list_of_lists[photo_num[p + 1] + 2 + i][0])
        peopleCoord2[i][1] = float(list_of_lists[photo_num[p + 1] + 2 + i][1])
        peopleSize2[i][0] = float(list_of_lists[photo_num[p + 1] + 2 + i][2])
        peopleSize2[i][1] = float(list_of_lists[photo_num[p + 1] + 2 + i][3])

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
            probs.append(full_prob)


        phiname = DiscreteFactor([name], [len(peopleCount)+1], [[0.8]+ probs])
        G.add_factors(phiname)
        G.add_edge(name, phiname)

    mat = np.ones((len(peopleCount)+1, len(peopleCount)+1))
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if i !=0 and j !=0:
                if i == j :
                    mat[i][j]=0.0
    combs = combinations(names, 2)
    for i in list(combs):
        phuname = DiscreteFactor([i[0], i[1]], [len(peopleCount)+1, len(peopleCount)+1], mat)
        G.add_factors(phuname)
        G.add_edge(i[0], phuname)
        G.add_edge(i[1], phuname)
    belief_propagation = BeliefPropagation(G)
    result = list(belief_propagation.map_query(G.get_variable_nodes()).values())
    result = [x - 1 for x in result]
    print(*result)

