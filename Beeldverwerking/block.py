class Block(object):
    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

        self.coordinate = ((right + left) / 2,(top + bottom) / 2)

    def getLocation(self):
        return self.coordinate
