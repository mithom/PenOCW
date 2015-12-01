import block

class Image:
    def __init__(self, img_width, img_height, blocks):
        self.img_width = img_width
        self.img_height = img_height
        self.blocks = blocks

    def get_width(self):
        return self.img_width

    def get_height(self):
        return self.img_height

    def get_blocks(self):
        return self.blocks

    def add_block(self, block):
        self.blocks.append(block)
