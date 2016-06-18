
class PositionList(list):
    def __init__(self, *args):
        list.__init__(self, *args)

    def set_range(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax



        # for h in h_list:

class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.val = None
