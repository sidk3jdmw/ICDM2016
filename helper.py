from patient import PatientList


class Huff():
    def __init__(self, alpha, beta, reachable_dist, threshold):
        self.alpha = alpha
        self.beta = beta
        self.threshold = threshold
        self.reachable_dist = reachable_dist

    def calc_huff(self, pat, h_list):
        prob = {}
        ad_sum = 0
        ad_list = [0] * len(h_list)
        # Sum
        for i, h in enumerate(h_list):
            dist = distance(pat, h)
            if dist <= self.reachable_dist:
                ad_list[i] = h.max_capacity * self.alpha / dist ** self.beta
                ad_sum += ad_list[i]

        # ignore
        if ad_sum == 0:
            return prob
        if self.threshold > 0:
            for i, ad in enumerate(ad_list):
                if ad / ad_sum < self.threshold:
                    ad_sum -= ad
                    ad_list[i] = 0

        for i, h in enumerate(h_list):
            if ad_list[i] != 0:
                prob[h] = ad_list[i] / ad_sum
        return prob

def distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def week_filter(pat_list, ws, we):
    new_pat_list = PatientList()
    for pat in pat_list:
        week = pat.date.isocalendar()[1]
        if ws <= week <= we:
            new_pat_list.append(pat)
    return new_pat_list
