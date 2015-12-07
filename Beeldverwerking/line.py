class Line:

    def __init__(self, *blocks):
        def sort_blocks(blocks):
            pass

        assert len(blocks) > 0
        self.blocks = blocks
        sort_blocks(self.blocks)

    def get_blocks(self):
        return self.blocks

    def get_first_block(self):
        return self.blocks[0]

    def get_rico(self):
        if len(self.blocks)== 1:
            return -10000
        else:
            return get_rico(self.blocks[0], self.blocks[-1])

    def get_type(self):
        if (True):
            return 'straight_line'
        elif (False):
            return 'right_turn'
        else:
            return 'left_turn'

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.blocks)


def get_rico(block1, block2):
    (x1,y1) = block1.get_middle()
    (x2,y2) = block2.get_middle()
    try:
        return (float(y2)-y1)/(x2-x1)
    except ZeroDivisionError:
        return -10000


