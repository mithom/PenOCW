#import Image
import math


class Block(object):
    def __init__(self, left, right, top, bottom, image):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.image = image
        self.coordinate = ((right + left) / 2,(top + bottom) / 2)

    def get_middle(self):
        return self.coordinate

    def get_image(self):
        return self.image

    def get_width(self):
        return self.right-self.left

    def get_height(self):
        return self.bottom - self.top

    def distance_from(self, block):
        return math.sqrt((block.get_middle()[0]-self.get_middle()[0])**2 + (block.get_middle()[1] - self.get_middle()[1])**2)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "[%i,%i]" % self.coordinate
