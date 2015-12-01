from line import Line, get_rico
from block import Block
import math


class Image:
    dist_threshold = 15
    radians_threshold = 15

    def __init__(self, img_width, img_height, blocks, block_restrictions):
        self.img_width = img_width
        self.img_height = img_height
        self.blocks = blocks
        self.block_restrictions = block_restrictions

    def get_img_width(self):
        return self.img_width

    def get_img_height(self):
        return self.img_height

    def get_blocks(self):
        return self.blocks

    def add_block(self, block):
        self.blocks.append(block)

    def get_main_line(self):
        blocks = self.get_blocks()
        if len(blocks) == 0:
            return Line(Block(self.img_width/2,self.img_width/2,min(1,self.img_height),min(1,self.img_height),self),
                        Block(self.img_width/2,self.img_width/2,self.img_height,self.img_height,self))
        elif len(blocks) == 1:
            return Line(blocks[0])
        else:
            blocks = []
            next_block = None
            prev_block = Block(self.get_img_width(), self.get_img_width(), self.get_img_height(), self.get_img_height(),self)
            for block in self.blocks:
                if block != prev_block and (next_block is None or
                                            (block.distance_from(prev_block) < next_block.distance_from(prev_block))):
                    next_block = block
            blocks.append(next_block)
            prev_block = next_block
            while True:
                blocks_in_range = []
                for block in self.blocks:
                    if block.distance_from(prev_block) < Image.dist_threshold and blocks != prev_block:
                        blocks_in_range.append(block)
                if len(blocks_in_range) == 0:
                    break

                if len(blocks)>1:
                    rico = get_rico(blocks[-2],blocks[-1])
                else:
                    rico = -10000
                smallest_dif = 95 #we do not want anything behind us
                next_block = None
                for block in blocks_in_range:
                    current_diff = math.tan(get_rico(blocks[-1], block)) - math.tan(rico)
                    if current_diff < smallest_dif:
                        smallest_dif = current_diff
                        next_block = block
                        if smallest_dif < Image.radians_threshold:
                            break
                if next_block is None:
                    break
                else:
                    blocks.append(next_block)

    def blocks_left_of_line(self):
        for b in self.get_blocks():
            if b.get_middle()[0] < self.get_main_line()[0]:
                return True
        return False

    def blocks_right_of_line(self):
        for b in self.get_blocks():
            if b.get_middle()[0] >= self.get_main_line()[0]:
                return True
        return False

    def block_on_line(self, block):
        if not (
            (block.get_middle()[0] < self.get_main_line()[0]) or (block.get_middle()[0] >= self.get_main_line()[0])):
            return True
        return False

    def get_blocks_on_line(self):
        blocks_on_line = []
        for b in self.get_blocks():
            if self.block_on_line(b):
                blocks_on_line.append(b)
        return blocks_on_line

    def get_first_block_on_line(self):
        lowest = 0
        first_block = None
        for b in self.get_blocks_on_main_line():
            if b.get_middle()[1] > lowest:
                first_block = b
                lowest = b.get_middle()[1]
        return first_block

    def get_structure(self):
        if self.is_intersection():
            return 'intersection'
        elif self.is_t_split():
            return 't_split'
        elif self.is_corner():
            return 'corner'
        elif self.is_turn():
            return 'turn'
        else:
            return 'Line'

    def is_intersection(self):
        return False

    def is_t_split(self):
        return False

    def is_corner(self):
        return False

    def is_turn():
        return False
