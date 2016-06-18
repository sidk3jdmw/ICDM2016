# import pandas as pd
# import matplotlib.pyplot as plt
import datetime as dt
from hospital import Hospital
from copy import deepcopy
import random
import heapq
from collections import Counter
from stack import XStackGroup, PerfectStackGroup
from patient import PatientList, week_filter
from position import PositionList, Position


class Evaluater(object):
    def __init__(self, h_list, p_list, t_cap, w_size, t_max_list, huff, allocate_method):
        self.h_list = h_list
        self.p_list = p_list
        self.t_cap = t_cap
        self.w_size = w_size
        self.huff = huff
        self.allocate_method = allocate_method
        self.t_list = [Hospital("Tmp-" + str(i), -1, -1, t_max_list[i]) for i in range(len(t_max_list))]
        self.a_list = self.h_list + self.t_list
        self.a_mapping = {a:i for i, a in enumerate(self.a_list)}
        self.rearrange_list = self.calc_rearrange_list()
        self.date_rearrange_list = self.calc_date_rearrange_list()
        self.counter = 0
        pass
    def calc_rearrange_list(self):
        q = 2
        f_week = self.p_list.fdate.isocalendar()[1]
        self.date_arange_list = []
        cur_week = f_week
        pointer = 0
        r_list = []
        for i, p in enumerate(self.p_list):
            if p.date.isocalendar()[1] - cur_week >= q:
                r_list.append((pointer, i - 1))
                pointer = i
                cur_week = p.date.isocalendar()[1]
                # self.date_arange_list.append()
        r_list.append((pointer, len(self.p_list) - 1))
        return r_list

    def calc_date_rearrange_list(self):
        q = 2
        f_date = self.p_list.fdate
        l_date = self.p_list.ldate
        pre_week = f_date.isocalendar()[1]
        pointer = 0
        i = 0
        r_list = []
        return [(0, (l_date - f_date).days)]
        while 1:
            if f_date > l_date:
                break
            if f_date.isocalendar()[1] - pre_week >= q:
                r_list.append((pointer, i - 1))
                pre_week = f_date.isocalendar()[1]
                pointer = i
            f_date += dt.timedelta(1)
            i += 1
        r_list.append((pointer, i - 1))
        return r_list

    def calc_huff_opt(self, pat):
        huff = self.huff
        t_list = self.t_list
        t_num = len(t_list)
        ad_list = [0] * t_num
        for i in range(t_num):
            ad_list[i] = huff.calc_single_ad(pat, t_list[0])

        prob_dict = huff.calc_huff_quick(pat, t_list, ad_list)
        return prob_dict

    def calc_huff(self, pat):
        return self.huff.calc_huff(pat, self.a_list)



    def eval_greedy_opt(self, pos):
        l_list = [a.max_capacity for a in self.a_list]
        t_list = self.t_list
        for i in range(len(pos)):
            t_list[i].x, t_list[i].y = pos[i].x, pos[i].y

        prob_dict_list = self.get_prob()
        stack_group = PerfectStackGroup(n=len(self.a_list), top=l_list, allocate_method=self.allocate_method)
        for i in range(100):
            come_record = self.emulating(prob_dict_list)
            in_record = self.get_in_record(come_record)
            stack_group.add_scenario(come_record, in_record)
        stack_group.normalize_scenario()
        result = stack_group.solve(self.t_cap, False)
        return result,

    def get_in_record(self, come_record):
        in_record = [[0] * (len(come_record[i]) + self.w_size - 1) for i in range(len(come_record))]
        for i in range(len(come_record)):
            for d, c in enumerate(come_record[i]):
                for w in range(self.w_size):
                    in_record[i][d + w] += c
        return in_record

    def get_result_and_peak(self, in_record, l_list):
        peak = [0] * len(l_list)
        result = 0
        for i, in_r in enumerate(in_record):
            for pat_num in in_r:
                v = 0
                if pat_num <= l_list[i]:
                    v = pat_num
                else:
                    v = l_list[i]
                result += v
                if v > peak[i]:
                    peak[i] = v
        return result, peak

    def get_result_and_peak_wrong(self, record, l_list):
        result = 0
        peak = [0] * len(l_list)
        sum_list = [0] * len(l_list)

        for i, a in enumerate(self.h_list):
            for d in range(0, self.date_rearrange_list[0][1] + 1):
                last_d = d - self.w_size
                if last_d >= 0:
                    sum_list[i] -= record[i][last_d]
                sum_list[i] += record[i][d]
                if sum_list[i] > l_list[i]:
                    # XXX WTF?
                    r = l_list[i] - sum_list[i] + record[i][d]
                    record[i][d] = r
                    sum_list[i] = l_list[i]
                else:
                    r = record[i][d]
                result += r
                if sum_list[i] > peak[i]:
                    peak[i] = sum_list[i]

        return result, peak

    def get_prob(self):

        p_list = self.p_list

        prob_dict_list = [{} for i in range(len(p_list))]
        for i, pat in enumerate(p_list):
            prob_dict_list[i] = self.calc_huff(pat)
        return prob_dict_list

    def emulating(self, prob_dict_list):
        mapping = self.a_mapping
        record = [[0] * self.p_list.total_days for i in range(len(self.a_list))]

        for j, pat in enumerate(self.p_list):
            prob_dict = prob_dict_list[j]
            rand = random.random()
            cum = 0
            for h, prob in prob_dict.items():
                cum += prob
                if rand <= cum:
                    record[mapping[h]][pat.day] += 1
                    break

        return record

def main():
    pass

if __name__ == "__main__":
    main()
