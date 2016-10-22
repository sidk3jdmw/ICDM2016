# import pandas as pd
from evaluator import Evaluater
from multiprocessing import Pool
import sys
import numpy as np
from helper import Huff, distance
from hospital import HospitalList, Hospital
from patient import PatientList
from position import PositionList, Position
import time

# Num of Process
process = 4

p = Pool(process)


def search_best_place(pos_list, e):
    result = p.map(lambda x: e.eval_greedy_opt([x]), pos_list)
    v = max(result)
    index = result.index(v)
    # print(v, pos_list[index].x, pos_list[index].y, e.counter)
    return pos_list[index], v

def get_init_pos_list(x_r, y_r, d):
    pos_list = PositionList()
    pos_list.xnum = len(np.arange(x_r[0], x_r[1], d))
    pos_list.ynum = len(np.arange(y_r[0], y_r[1], d))
    for y in np.arange(y_r[0], y_r[1], d):
        for x in np.arange(x_r[0], x_r[1], d):
            pos_list.append(Position(x, y))
    return pos_list


def density_filter(pos_list, patients, density, dist):
    new_pos_list = []
    density_block = [0] * len(pos_list)
    gap = distance(pos_list[0], pos_list[1])
    dist_b = int(dist / gap + 1)
    xnum = pos_list.xnum
    xmin, ymin = pos_list.xmin, pos_list.ymin
    counter = 0
    for pat in patients:
        pat_x, pat_y = pat.x - xmin, pat.y - ymin
        pat_block = int(pat_x / gap) + int(pat_y / gap) * xnum
        for y in range(-dist_b, dist_b + 1):
            x_r = dist_b - abs(y)
            for x in range(-x_r, x_r + 1):
                try:
                    density_block[pat_block + x + y * xnum] += 1
                    counter += 1
                except IndexError:
                    pass
    for i, d in enumerate(density_block):
        if d >= density:
            new_pos_list.append(pos_list[i])
    return new_pos_list

def main():
    # algorithm arguments init
    density = 3000
    dist = 0.02
    step = 0.005

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

    # record variables
    result_pos = []
    start_time = time.time()


    hospital_list = HospitalList()
    hospital_list.read_file(hospital_filename)

    pat_list = PatientList()
    pat_list.read_file(patient_filename)


    pos_list = get_init_pos_list((pat_list.xmin, pat_list.xmax), (pat_list.ymin, pat_list.ymax), step)
    pos_list.set_range(pat_list.xmin, pat_list.xmax, pat_list.ymin, pat_list.ymax)
    pos_list = density_filter(pos_list, pat_list, density, dist)

    print("Num of Selectable Position: ", len(pos_list))

    for i in range(tmp_num):
        tmp_max = tmp_max_list[i]
        e = Evaluater(hospital_list, pat_list, total_capacity, window_size, [tmp_max], huff, method)
        pos, v = search_best_place(pos_list, e)
        pos_list.sort(key=lambda p: p.val, reverse=True)
        result_pos.append(pos)
        new_h = Hospital("Tmp-" + str(i), pos.x, pos.y, tmp_max)
        hospital_list.append(new_h)
        del e

    print "\nResult:"
    print v[0]
    print "\nPosition:"
    for i in range(len(result_pos)):
        print "%f, %f" % (result_pos[i].x, result_pos[i].y)
    # print(v, result_pos)

if __name__ == "__main__":
    main()
