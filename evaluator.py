from hospital import Hospital
import random
from stack import PerfectStackGroup


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
        self.counter = 0
        pass

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
