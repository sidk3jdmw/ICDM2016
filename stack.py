from collections import Counter
import heapq
class StackGroup():
    def __init__(self, n, top, allocate_method):
        self.n = n
        self.top = top
        self.stacks = [[0.] * top[i] for i in range(n)]
        self.scenario_num = 0
        self.solve = self.select_method(allocate_method)
        pass

    def select_method(self, allocate_method):
        if allocate_method == "Greedy":
            return self.greedy_solve
        elif allocate_method == "DP":
            return self.dp_solve
    def normalize_scenario(self):
        stacks = self.stacks
        scenario_num = self.scenario_num
        n, top = self.n, self.top
        for i in range(n):
            for j in range(top[i]):
                stacks[i][j] /= scenario_num

    def stack_to_item_dp(self):
        stacks = self.stacks
        # item (weight, value)
        grouped_items = [[(0, 0)] * (self.top[i] + 1) for i in range(self.n)]
        for i in range(self.n):
            for j in range(1, self.top[i] + 1):
                grouped_items[i][j] = (j , stacks[i][j - 1] + grouped_items[i][j - 1][1])
        return grouped_items

    def dp_solve(self, pop_times, up_to_down):
        # if up_to_down:
            # pass
        # else:
            # pass
        f = [0] * (pop_times + 1)
        grouped_items = self.stack_to_item_dp()
        # print([len(g) for g in grouped_items)
        for g_i in grouped_items:
            for space in range(pop_times, 0, -1):
                for w, v in g_i:
                    if space - w >= 0:
                        f[space] = max(f[space], f[space - w] + v)
        return f[pop_times]

    def stack_to_item_greedy(self):
        stacks = self.stacks
        # item (v/w, weight, value, group)
        # grouped_items = [[(0., 0., 0., 0)] * (self.top[i] + 1) for i in range(self.n)]
        all_items = []
        for i in range(self.n):
            g = [(0, 0, 0, 0)] * (self.top[i] + 1)
            for j in range(1, self.top[i] + 1):
                value = stacks[i][j - 1] + g[j - 1][1]
                g[j] = (value / j, j, value, i)
            all_items.extend(g)
        return all_items

    def greedy_solve(self, pop_times, up_tp_down):
        stacks = self.stacks
        result = 0
        for s in stacks:
            s.reverse()
        heap = [(-s[-1], i) for i, s in enumerate(stacks)]
        heapq.heapify(heap)
        for i in range(pop_times):
            v, index = heapq.heappop(heap)
            result += v
            try:
                new_v = stacks[index].pop()
                heapq.heappush(heap, (-new_v, index))
            except:
                pass


        # result = 0
        # selected = [False] * self.n
        # all_items = self.stack_to_item_greedy()
        # all_items.sort(reverse=True)
        # for item in all_items:
            # cp, weight, value, group = item
            # if not selected[group] and pop_times >= weight:
                # pop_times -= weight
                # selected[group] = True
                # result += value
        # print(pop_times)
        return -result

class XStackGroup(StackGroup):
    def add_scenario(self, come_record, in_record):
        self.scenario_num += 1
        stacks = self.stacks
        for i in range(self.n):
            in_record[i].append(0)
            max_cap = self.top[i]
            in_record[i] = list(map(lambda x: x if x <= max_cap else max_cap, in_record[i]))
            temp_list = list(Counter(in_record[i]).items())
            temp_list.sort()
            # remove 0 amounts
            temp_list[0] = (0, 0)
            if temp_list[-1][0] != max_cap:
                temp_list.append((max_cap, 0))

            last_index = 0
            cum_val = sum(t[1] for t in temp_list)
            for j in range(1, len(temp_list)):
                cum_val -= temp_list[j - 1][1]
                for k in range(last_index, temp_list[j][0]):
                    stacks[i][k] += cum_val
                last_index = temp_list[j][0]
            # print(sum(stacks[0]))
            # print(temp_list)
            # print(stacks[0])
            # exit()
        pass


class PerfectStackGroup(StackGroup):
    def add_scenario(self, come_record, in_record):
        self.scenario_num += 1
        stacks = self.stacks
        for i, sk in enumerate(stacks):
            pre_val = 0
            c_r, i_r = come_record[i], in_record[i]
            for j in range(self.top[i]):
                tmp = self.get_result(c_r, i_r, j + 1)
                sk[j] += tmp - pre_val
                pre_val = tmp
        pass

    def get_result(self, c_r, i_r, res):
        result = 0
        for c, i in zip(c_r, i_r):
            if i <= res:
                result += c
            else:
                result += max(0, res - i)
            pass
        return result


def main():
    xs = XStackGroup(n=2, top=[10, 10])
    xs.add_scenario([], [[0, 2, 2, 6, 8], [3,3,2,1]])
    print(xs.stacks[0])

if __name__ == "__main__":
    main()

