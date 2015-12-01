import block

class Image:
    def __init__(self, img_width, img_height, blocks, px):
        self.img_width = img_width
        self.img_height = img_height
        self.blocks = blocks
		self.px = px

    def get_width(self):
        return self.img_width

    def get_height(self):
        return self.img_height

    def get_blocks(self):
        return self.blocks

    def add_block(self, block):
        self.blocks.append(block)

	def get_main_line(self):
		blocks = self.get_blocks()
		if len(blocks) == 0:
			return int(self.get_width()/2)
		if len(blocks) == 1:
			return blocks[0].getLocation()[0]
		else:
			return None

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
			return 'line'

	def is_intersection(self):
		return False

	def is_t_split(self):
		return False

	def is_corner(self):
		return False

	def is_turn():
		return False
