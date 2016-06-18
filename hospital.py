import csv

class HospitalList(list):
    def __init__(self, *args):
        list.__init__(self, *args)

    def read_file(self, filename):
        f = open(filename, "r")
        # escape first line
        f.readline()
        for row in csv.reader(f, delimiter="\t"):
            h = Hospital(row[0], float(row[1]), float(row[2]), int(row[3]))
            self.append(h)

class Hospital(object):
    def __init__(self, name, x, y, max_capacity):
        self.name = name
        self.x = x
        self.y = y
        self.max_capacity = max_capacity
        # self.min_capacity = min_capacity
        self.dist_list = []

    # def __hash__(self):
        # return hash(self.name)

