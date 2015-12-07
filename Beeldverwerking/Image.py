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
        self.line = self._get_main_line()

    def get_img_width(self):
        return self.img_width

    def get_img_height(self):
        return self.img_height

    def get_blocks(self):
        return self.blocks

    def add_block(self, block):
        self.blocks.append(block)

    def get_main_line(self):
        return self.line

    def _get_main_line(self):
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
            while True:
                prev_block = blocks[-1]
                blocks_in_range = []
                for block in self.blocks:
                    if block.distance_from(prev_block) < Image.dist_threshold and block not in blocks:  # TODO: lijn die terugkeert ondersteunen
                        blocks_in_range.append(block)
                if len(blocks_in_range) == 0:
                    break
                elif len(blocks)>1:
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
            return Line(*blocks)

    def blocks_left_of_line(self, line):
        blocks_left = []
        rico = line.get_rico()
        if rico == None:
            return None
        elif rico < 0:
            rico_sign = -1
        else:
            rico_sign = 1
        for block1 in self.get_blocks():
            block_is_left = True
            if not self.block_on_line(block1, line):
                for block2 in line.get_blocks():
                    if not ((block1.get_middle()[0] < block2.get_middle()[0]) or (block1.get_middle()[1]*rico_sign > block2.get_middle()[1]*rico_sign)): #hoger als rico > 0, lager als rico < 0
                        block_is_left = False
                        break
                if block_is_left:
                    blocks_left.append(block1)
        return blocks_left


    def blocks_right_of_line(self, line):
        blocks_right = []
        rico = line.get_rico()
        if rico == None:
            return None
        elif rico < 0:
            rico_sign = -1
        else:
            rico_sign = 1
        for block1 in self.get_blocks():
            block_is_right = True
            if not self.block_on_line(block1, line):
                for block2 in line.get_blocks():
                    if not ((block1.get_middle()[0] > block2.get_middle()[0]) or (-(block1.get_middle()[1]*rico_sign) > -(block2.get_middle()[1]*rico_sign))): #hoger als rico < 0, lager als rico > 0
                        block_is_right = False
                        break
                if block_is_right:
                    blocks_right.append(block1)
        return blocks_right

    def block_on_line(self, block, line):
        if block in line.get_blocks():
            return True
        return False

    def get_structure(self):
        if self.is_intersection():
            return 'intersection'
        elif self.is_t_split():
            return 't_split'
        elif self.is_corner():
            return 'corner'
        else:
            return 'Line'

    def is_intersection(self):
        return False

    def is_t_split(self):
        return False

    def is_corner(self):
        return False

