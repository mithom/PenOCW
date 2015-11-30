class Block(object):
    def __init__(self, coordinates=(0, 0)):
        self.coordinate = coordinates

    def getLocation(self):
        return self.coordinate
