from line import Line, get_rico
from block import Block
import math


class Image:
    dist_threshold = 15

    def __init__(self, img_width, img_height, blocks):
        self.img_width = img_width
        self.img_height = img_height
        self.blocks = []
        for block in blocks:
            self.add_block(block)

    def get_img_width(self):
        return self.img_width

    def get_img_height(self):
        return self.img_height

    def get_blocks(self):
        return self.blocks

    def add_block(self, block):
        self.blocks.append(block)
        block.set_image(self)

    def clear_blocks(self):
        self.blocks[:] = []

    def get_main_line(self):
        blocks = self.get_blocks()
        if len(blocks) == 0:
            block = Block(self.img_width / 2, self.img_width / 2, min(1, self.img_height), min(1, self.img_height))
            self.add_block(block)
            return Line(block,
                        Block(self.img_width / 2, self.img_width / 2, 0, 0))
        elif len(blocks) == 1:
            return Line(blocks[0], Block(blocks[0].get_middle()[0],blocks[0].get_middle()[0],0,0))
        else:
            blocks = []
            next_block = None
            prev_block = Block(self.get_img_width() / 2, self.get_img_width() / 2, self.get_img_height(),
                               self.get_img_height())
            for block in self.get_blocks():
                if block != prev_block and (next_block is None or
                                            (block.distance_from(prev_block) < next_block.distance_from(prev_block))):
                    next_block = block
            blocks.append(next_block)
            while True:
                prev_block = blocks[-1]
                blocks_in_range = []
                for block in self.get_blocks():
                    if block.distance_from(prev_block) < Image.dist_threshold \
                            and block not in blocks and block.get_middle()[1] <= prev_block.get_middle()[1]:  # TODO: lijn die terugkeert ondersteunen
                        blocks_in_range.append(block)
                if len(blocks_in_range) == 0:
                    break
                elif len(blocks)>1:
                    rico = get_rico(blocks[-2],blocks[-1])
                else:
                    rico = -10000
                smallest_dif = math.pi/2.2  #we do not want anything behind us
                next_block = None
                for block in blocks_in_range:
                    current_diff = Image.calculate_diff(math.atan(get_rico(prev_block, block)), math.atan(rico))
                    if current_diff < smallest_dif:
                        smallest_dif = current_diff
                        next_block = block
                if next_block is None:
                    break
                else:
                    blocks.append(next_block)
            try:
                x = (-blocks[-1].get_middle()[1])/get_rico(blocks[0],blocks[-1])+blocks[-1].get_middle()[0]
                blocks.append(Block(x,x,0,0))
            except ZeroDivisionError:
                print get_rico(blocks[0],blocks[-1])
                print blocks
                print "-----------STOP---------------------------------------------------------------"
            return Line(*blocks)

    @staticmethod
    def calculate_diff(radians1, radians2):
        if math.copysign(radians1, radians2) == radians1:
            return abs(radians1 - radians2)
        else:
            return math.pi - abs(radians1) - abs(radians2)

    def get_blocks_left_of_line(self, line):
        blocks_left = []
        rico = line.get_rico()
        if rico is None:
            return None
        elif rico < 0:
            rico_sign = -1
        else:
            rico_sign = 1
        for block1 in self.get_blocks():
            block_is_left = True
            if not self.is_block_on_line(block1, line):
                for block2 in line.get_blocks():
                    if not ((block1.get_middle()[0] < block2.get_middle()[0]) or (block1.get_middle()[1]*rico_sign > block2.get_middle()[1]*rico_sign)): #hoger als rico > 0, lager als rico < 0
                        block_is_left = False
                        break
                if block_is_left:
                    blocks_left.append(block1)
        return blocks_left


    def get_blocks_right_of_line(self, line):
        blocks_right = []
        rico = line.get_rico()
        if rico is None:
            return None
        elif rico < 0:
            rico_sign = -1
        else:
            rico_sign = 1
        for block1 in self.get_blocks():
            block_is_right = True
            if not self.is_block_on_line(block1, line):
                for block2 in line.get_blocks():
                    if not ((block1.get_middle()[0] > block2.get_middle()[0]) or (-(block1.get_middle()[1]*rico_sign) > -(block2.get_middle()[1]*rico_sign))): #hoger als rico < 0, lager als rico > 0
                        block_is_right = False
                        break
                if block_is_right:
                    blocks_right.append(block1)
        return blocks_right

    def is_block_on_line(self, block, line):
        if block in line.get_blocks():
            return True
        return False

    # def blocks_form_line_to_main(self, blocks, main_line):
    #     rico_main = main_line.get_rico()
    #     if len(blocks) < 2:
    #         return False
    #     else:
    #         ricos_blocks = self.get_lines_through_blocks(blocks)
    #         for rico_block in ricos_blocks:
    #             if ((math.atan(rico_block) < (1/math.atan(rico_main)) + math.pi/3) and (math.atan(rico_block) > (1/math.atan(rico_main)) - math.pi/3)):
    #                 return True
    #         return False
    #
    # def get_lines_through_blocks(self, blocks):
    #     ricos_blocks = []
    #     for i in xrange(len(blocks)):
    #         for j in xrange(i,len(blocks)):
    #             ricos_blocks.append(get_rico(blocks[i], blocks[j]))
    #     return ricos_blocks
        

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

