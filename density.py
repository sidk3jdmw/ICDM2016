# import pandas as pd
from evaluator import Evaluater
import sys
import numpy as np
from helper import Huff, distance
from hospital import HospitalList, Hospital
from patient import PatientList
from position import PositionList, Position
import time


def get_init_pos_list(x_r, y_r, d):
    pos_list = PositionList()
    pos_list.xnum = len(np.arange(x_r[0], x_r[1], d))
    pos_list.ynum = len(np.arange(y_r[0], y_r[1], d))
    for y in np.arange(y_r[0], y_r[1], d):
        for x in np.arange(x_r[0], x_r[1], d):
            pos_list.append(Position(x, y))
    return pos_list


def density_sorter(pos_list, patients):
    density_block = [0] * len(pos_list)
    gap = distance(pos_list[0], pos_list[1])
    xnum = pos_list.xnum
    xmin, ymin = pos_list.xmin, pos_list.ymin
    for pat in patients:
        pat_x, pat_y = pat.x - xmin, pat.y - ymin
        pat_block = int(pat_x / gap) + int(pat_y / gap) * xnum
        density_block[pat_block] += 1
    for i in range(len(density_block)):
        pos_list[i].density = density_block[i]
    pos_list.sort(key = lambda x: x.density, reverse=True)
    return pos_list


def no_hospital_around(pos, h_list, dist):
    flag = True
    for h in h_list:
        if distance(pos, h) <= dist:
            flag = False
            break
    return flag


def main():
    # algorithm arguments init
    step = 0.001
    # evaluator arguments init
    total_capacity = 3000
    window_size = 3
    tmp_num = 2
    tmp_max_list = [90] * tmp_num
    method = "DP"

    # huff arguments init
    alpha = 1
    beta = 1
    ignore_prob = 0.01
    reachable_dist = 0.02
    huff = Huff(alpha, beta, reachable_dist, ignore_prob)

    # file name
    patient_filename = sys.argv[1]
    hospital_filename = sys.argv[2]


    # build hospital list
    hospital_list = HospitalList()
    hospital_list.read_file(hospital_filename)

    pat_list = PatientList()
    pat_list.read_file(patient_filename)



    pos_list = get_init_pos_list((pat_list.xmin, pat_list.xmax), (pat_list.ymin, pat_list.ymax), step)

    pos_list.set_range(pat_list.xmin, pat_list.xmax, pat_list.ymin, pat_list.ymax)
    pos_list = density_sorter(pos_list, pat_list)
    tmp_list = []
    result_list = []
    p_list = []
    for ar in range(0, 50 + 1):
        arr = 0.002 * ar
        for i, pos in enumerate(pos_list):
            if no_hospital_around(pos, hospital_list + tmp_list, arr):
                new_h = Hospital("Tmp-" + str(i), pos.x, pos.y, tmp_max_list[0])
                tmp_list.append(new_h)

            if len(tmp_list) == tmp_num:
                break


        e = Evaluater(hospital_list, pat_list, total_capacity, window_size, tmp_max_list, huff, method)
        r = e.eval_greedy_opt([t for t in tmp_list])
        p_list.append([(t.x, t.y) for t in tmp_list])
        del e
        result_list.append(r)
    value = max(result_list)
    index = result_list.index(value)

    print "\nResult:"
    print value[0]
    print "\nPosition:"
    for i in range(len(p_list[index])):
        print "%f, %f" % p_list[index][i]

if __name__ == "__main__":
    main()
