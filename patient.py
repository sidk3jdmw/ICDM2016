import csv
# from helper import Huff
import datetime as dt

class PatientList(list):
    def __init__(self, *args):
        list.__init__(self, *args)

    def read_file(self, filename):
        f = open(filename, "r")
        # escape first line
        f.readline()

        for row in csv.reader(f, delimiter="\t"):
            date = dt.datetime.strptime("2015/" + row[5], "%Y/%m/%d")
            p = Patient(float(row[9]), float(row[10]), date)
            self.append(p)
        self.update_info()

    def update_info(self):
        self.xmin = min(p.x for p in self)
        self.xmax = max(p.x for p in self)
        self.ymin = min(p.y for p in self)
        self.ymax = max(p.y for p in self)

        self.fdate = self[0].date
        self.ldate = self[-1].date
        self.total_days = (self.ldate - self.fdate).days + 1

        for p in self:
            p.day = (p.date - self.fdate).days

    def build_relations(self, h_list, huff):
        for pat in self:
            pat.build_relation(h_list, huff)
        # self.relation = {}
        pass

    def append_relations(self, h_list, huff):
        for pat in self:
            pat.append_relation(h_list, huff)

class Patient(object):
    def __init__(self, x, y, date):
        self.x = x
        self.y = y
        self.date = date
        self.relation = {}
        self.ad_sum = None
        self.w = 1.

    def build_relation(self, h_list, huff):
        self.ad_sum = 0
        huff.set_ad(self, h_list)
        huff.set_prob_quick(self)
        # self.relation = {}
        pass

    def append_relation(self, h_list, huff):
        huff.set_ad(self, h_list)
        huff.set_prob_quick(self)

def week_filter(pat_list, ws, we):
    new_pat_list = PatientList()
    for pat in pat_list:
        week = pat.date.isocalendar()[1]
        if ws <= week <= we:
            new_pat_list.append(pat)
    return new_pat_list


def main():
    pat_list = PatientList()
    pat_list.read_file("sorted.tsv")
    print(len(pat_list))
    for i in range(2, 50, 2):
        new_pat_list = week_filter(pat_list, i, i + 1);
        print(i, len(new_pat_list))
    # print(len(new_pat_list))
    # new_pat_list = week_filter(pat_list, 15, 16);
    # print(len(new_pat_list))

if __name__ == "__main__":
    main()
