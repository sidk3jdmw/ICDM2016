


class Huff():
    def __init__(self, alpha, beta, reachable_dist, threshold):
        self.alpha = alpha
        self.beta = beta
        self.threshold = threshold
        self.reachable_dist = reachable_dist

    def set_ad(self, p, h_list):
        alpha = self.alpha
        beta = self.beta
        ad_sum = p.ad_sum
        for h in h_list:
            d = distance(p, h)
            if d > self.reachable_dist:
                continue
            ad = h.max_capacity ** alpha / d ** beta
            p.relation[h] = [ad, None]
            ad_sum += ad
        p.ad_sum = ad_sum

    def set_prob_quick(self, p):
        new_ad_sum = 0
        threshold = self.threshold
        if p.ad_sum == 0:
            p.relation.clear()
            return
        for h, val in p.relation.items():
            ad = p.relation[h][0]
            prob = ad / p.ad_sum
            if prob < threshold:
                p.relation.pop(h)
            else:
                new_ad_sum += ad

        p.ad_sum = new_ad_sum
        for h, val in p.relation.items():
            p.relation[h][1] = p.relation[h][0] / new_ad_sum

    def calc_huff_quick(self, pat, t_list, ad_list):
        ad_sum = pat.ad_sum
        new_ad_sum = ad_sum
        prob = {}
        if ad_sum == 0:
            ad_sum = 1e-10
            pass
        break_flag = True
        t_relation = {}
        for ad, t in zip(ad_list, t_list):
            if ad / ad_sum < self.threshold:
                pass
            else:
                new_ad_sum += ad
                t_relation[t] = (ad, 0)
                break_flag = False
        if break_flag:
            prob = {h:v[1] for h, v in pat.relation.items()}
            return prob

        new_pat_relation = dict(pat.relation)
        new_pat_relation.update(t_relation)
        ad_sum = new_ad_sum
        new_ad_sum = ad_sum
        for h, v in new_pat_relation.items():
            prob[h] = v[0] / ad_sum
            if v[0] / ad_sum < self.threshold:
                new_pat_relation.pop(h)
                new_ad_sum -= v[0]
        if new_ad_sum == ad_sum:
            return prob

        prob = {}
        for h, v in new_pat_relation.items():
            prob[h] = v[0] / new_ad_sum

        return prob

    def calc_single_ad(self, p, h):
        d = distance(p, h)
        if d > self.reachable_dist:
            return 0.
        ad = h.max_capacity * self.alpha / d ** self.beta
        return ad

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

