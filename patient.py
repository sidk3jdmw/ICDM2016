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
            date = dt.datetime.strptime(row[2], "%Y/%m/%d")
            p = Patient(float(row[0]), float(row[1]), date)
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


class Patient(object):
    def __init__(self, x, y, date):
        self.x = x
        self.y = y
        self.date = date
        self.relation = {}
        self.ad_sum = None
        self.w = 1.



def main():
    pass

if __name__ == "__main__":
    main()
