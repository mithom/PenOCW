from Image import Image
from block import Block
import cv2 as cv

min_width = 1
max_width = 9
min_length = 1
max_length = 9
image = Image(65,40,[],(min_width, max_width, min_length, max_length))
blocks =[[24,33], [3,30], [11,30], [18,30], [32,30], [40,30], [47,30], [24,26], [24,19], [25,13]]
for block in blocks:
    image.add_block(Block(block[0], block[0], block[1], block[1], image))
line = image.get_main_line().get_blocks()
print line