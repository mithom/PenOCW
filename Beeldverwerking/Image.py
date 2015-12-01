import block

class Image:
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
			return None
		if len(blocks) == 1:
			return (blocks[0].getLocation()[0] - int(blocks[0].get_width()/2), blocks[0].getLocation()[0] + int(blocks[0].get_width()/2))
		else:
			return None

	def blocks_left_of_line(self):
		for block in self.get_blocks():
            if block.getLocation()[0] < self.get_main_line()[0]:
                return True
        return False

	def blocks_right_of_line(self):
		for block in self.get_blocks():
            if block.getLocation()[0] >= self.get_main_line()[0]:
                return True
        return False

	def block_on_line(self, block):
		if not ((block.getLocation()[0] < self.get_main_line()[0]) or (block.getLocation()[0] >= self.get_main_line()[0])):
            return True
        return False

	def get_blocks_on_line(self):
		blocks_on_line = []
		for block in self.get_blocks():
			if self.block_on_line(block):
				blocks_on_line.append(block)
		return blocks_on_line

	def get_first_block_on_line(self):
		lowest = 0
		first_block = None
		for block in self.get_blocks_on_main_line():
			if block.getLocation()[1] > lowest:
				first_block = block
				lowest = block.getLocation()[1]
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
			return 'line'

	def is_intersection(self):
		return False

	def is_t_split(self):
		return False

	def is_corner(self):
		return False

	def is_turn():
		return False
