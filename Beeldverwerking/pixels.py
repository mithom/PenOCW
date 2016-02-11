# Importing needed modules
import cv2 as cv
import math
from block import Block
import line as lines
import Image
import copy
import beeldverwerkingNameSpace
from socketIO_client import SocketIO
import urllib
import numpy as np
import time
import logging; logging.basicConfig(level=logging.DEBUG)

url = '192.168.137.78'
#url="127.0.0.1"
port = 4848
current_route_description = []
if __name__ == "__main__":
    socketIO = SocketIO(url, port, verify = False)
    beeldverwerking_namespace = socketIO.define(beeldverwerkingNameSpace.BeeldverwekingNameSpace, '/beeldverwerking')

## intitializing variebles needed for steering
street_counter = 0
last_street = 10


# Stream capturing code copied from
# http://stackoverflow.com/questions/24833149/track-objects-in-opencv-from-incoming-mjpeg-stream


# Searching blocks
def remove_whites(px, left, right, bottom, top):
    for i in xrange(left, right + 1):
        for j in xrange(bottom, top, -1):
            px[j][i] = 0
    return px


def check_right(index):
    if index > (img_width - 1):
        index = (img_width - 1)
    return index


def check_top(index):
    if index < 0:
        index = 0
    return index


def find_whites(y,x,direction):
    count = 0
    if direction == 'left':
        while x > 0:
            x -= 1
            if px[y][x]==255:
                count += 1
            else:
                break
    elif direction == 'right':
        while x < (img_width-1):
            x += 1
            if px[y][x]==255:
                count += 1
            else:
                break
    elif direction == 'up':
        while y > 0:
            y -= 1
            if px[y][x]==255:
                count += 1
            else:
                break
    else:
        while y < (img_height-1):
            y += 1
            if px[y][x]==255:
                count += 1
            else:
                break
    if direction == 'up' or direction == 'down':
        if count > max_length/2:
            count = max_length/2
    else:
        if count > max_width/2:
            count = max_width/2
    return count


def check_middle_x(y,x):
    left = find_whites(y,x,'left')
    right = find_whites(y,x,'right')
    if left > right:
        return True
    if abs(left-right)>1:
        return False
    else:
        return True

def check_middle_y(y,x):
    up = find_whites(y,x,'up')
    down = find_whites(y,x,'down')
    if down > up:
        return True
    if abs(up-down)>1:
        return False
    else:
        return True


def wide_enough(row, column):
    for i in xrange(min_width, max_width):
        a = column + i
        a = check_right(a)
        if px[row][a] == 255:
            width = a - column
            return width, True
    return 0, False


def diagonal_check(row, column):
    for i in xrange(min_width, max_width):
        a = column + i
        a = check_right(a)
        for i in xrange(min_length, max_length):
            b = row - i
            b = check_top(b)
            if px[b][a] == 255:
                return True
    return False


def long_enough(row, column):
    for i in xrange(min_length, max_length):
        a = row - i
        a = check_top(a)
        if px[a][column] == 255:
            length = row - a
            return length, True
    return 0, False


def go_first_block(power, line):
    block = line.get_first_block()
    location = block.get_middle()
    width = block.get_image().get_img_width()
    height = block.get_image().get_img_height()
    mid_block = Block(width/2, width/2, height, height)
    rico = lines.get_rico(block,mid_block)
    radians = math.atan(rico)
    if abs(radians)<math.pi/4:
        if radians >0: #positief = naar links draaien
            beeldverwerking_namespace.set_powers(0, 75)
        else:
            beeldverwerking_namespace.set_powers(75, 0)
    else:
        degrees = int(math.copysign(90,radians) -math.degrees(radians))
        beeldverwerking_namespace.set_powers(60- degrees/4, 60+degrees/4)


def go_first_block_2(power, line):
    block = line.get_first_block()
    location = block.get_middle()
    width = block.get_image().get_img_width()
    height = block.get_image().get_img_height()
    mid_block = Block(width / 2, width / 2, height, height)
    rico = lines.get_rico(block,mid_block)
    radians = math.atan(rico)
    if abs(radians)<math.pi/4 and location[1] < height-7:
        if radians >0: #positief = naar links draaien
            beeldverwerking_namespace.set_powers(0, 60)
        else:
            beeldverwerking_namespace.set_powers(60, 0)
    else:
        radians = math.atan(line.get_rico())
        compensation = int(math.degrees(Image.Image.calculate_diff(math.pi, radians)))
        if not width/2 +5 > location[0] > width/2-5:
            compensation -= (location[0] - width/2)
        beeldverwerking_namespace.set_powers(power- compensation/4, power+compensation/4)


def is_crossing(main_line, blocks):
    if len(blocks) >= 2:
        for i in xrange(len(blocks)-1):
            for block2 in blocks[i+1:]:
                difference = Image.Image.calculate_diff(
                    math.atan(lines.get_rico(blocks[i], block2)),
                    math.atan(main_line.get_rico()))
                if math.radians(100) > difference > math.radians(80):
                    return True
    return False
if __name__ == "__main__":
    stream = urllib.urlopen('http://%(url)s:%(port)i//video_feed.mjpg' % {'url': url, 'port': port})
byte = ''
while True and __name__ == "__main__":
    a = -1
    b = -1
    while a == -1 or b == -1:
        byte += stream.read(1024)
        a = byte.find('\xff\xd8')
        b = byte.find('\xff\xd9')
    if a != -1 and b != -1:
        start = time.time()
        jpg = byte[a:b + 2]
        byte = byte[b + 2:]
        frame = cv.imdecode(np.fromstring(jpg, dtype=np.uint8), 1)
        #frame = cv.resize(frame, (2592, 1944), interpolation=cv.INTER_AREA)

        # Image loading
        # frame = cv.imread('C:\\Users\\Gilles\\Dropbox\\Gilles\\Documenten\\School\\PenO_CW\\repo\\Beeldverwerking\\pi_photos\\cam0.jpg', 0)

        gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

        # Gaussian blur
        blur = cv.GaussianBlur(gray, (5, 5), 0)


        #frame = None

        threshold = 256

        # Threshold voor bw bepalen adh gemiddelde grijswaarde over de foto
        hist = None
        hist = cv.calcHist([blur], [0], None, [32], [0, 256])
        for x in xrange(31, 15, -1): # werkt goed, behalve grote schaduwvlekken
            if sum(hist[x] > 0):
                threshold = (x - 6) * 8 + 4
                hist = None
                break

        hist = None
        x = None

        blur = cv.resize(blur, (2592, 1944), interpolation=cv.INTER_NEAREST)  # TODO: check waarvoor deze resize is, want is vreemd

        # Thresholding
        ret, bw = cv.threshold(blur, threshold, 255, cv.THRESH_BINARY)


        # Cutting
        #cut1 = bw[bw.shape[0] / 3:bw.shape[0]]
        #cut2 = cut1[:, cut1.shape[1] * 1 / 4:cut1.shape[1] * 3 / 4]

        # Variable declaration
        bw_width = bw.shape[1]
        bw_height = bw.shape[0]
        img_division = 50
        min_width = 2
        max_width = 9
        min_length = 1
        max_length = 9
        number_blocks = 0

        # Pixelation
        px = cv.resize(bw, (bw_width / img_division, bw_height / img_division), interpolation=cv.INTER_NEAREST)

        img_width = px.shape[1]
        img_height = px.shape[0]
        image = Image.Image(img_width, img_height, [])  # TODO: is dit wel de juiste params van shape?

        pxbackup = copy.deepcopy(px)
        pxback2 = cv.resize(pxbackup, (bw_width/4, bw_height/4), interpolation=cv.INTER_NEAREST)
        cv.imwrite('C:\\Users\\Gilles\\Desktop\\screens\\5_pxbackup.jpg', pxback2)
        #TODO: middelpunt naar links laten verschuiven indien nodig

        for r in xrange(img_height - 1, 0, -1):
            for c in xrange(0, img_width - 1, 1):
                if px[r][c] == 255:
                    if r != 0 and c != (img_width - 1):
                        if px[r - 1][c] == 0 or px[r][c + 1] == 0:
                            px[r][c] = 0
                        else:
                            width, wide = wide_enough(r, c)
                            length, long = long_enough(r, c)
                            diagonal = diagonal_check(r, c)
                            if wide and long and diagonal:
                                # t = c
                                # u = c + width
                                # v = r
                                # w = r - length
                                y = r - 1
                                x = c + 1
                                y = check_top(y)
                                x = check_right(x)
                                flag1 = False
                                flag2 = False
                                while (check_middle_x(y,x) == False and flag1 == False) or \
                                        (check_middle_y(y,x) == False and flag2 == False):
                                    if check_middle_x(y,x) == False and flag1 == False:
                                        last_x = x
                                        x += 1
                                        x = check_right(x)
                                        if x == last_x:
                                            flag1 = True
                                    if check_middle_y(y,x) == False and flag2 == False:
                                        last_y = y
                                        y -= 1
                                        check_top(y)
                                        if y == last_y:
                                            flag2 = True
                                t = x - find_whites(y,x,'left')
                                u = x + find_whites(y,x,'right')
                                v = y + find_whites(y,x,'down')
                                w = y - find_whites(y,x,'up')
                                new_block = Block(t, u, v, w)
                                image.add_block(new_block)
                                px = remove_whites(px, t, u, v, w)
                                # foto = cv.resize(px, (bw_width/4, bw_height/4), interpolation=cv.INTER_NEAREST)
                                # cv.imshow('f', foto)
                                # cv.waitKey(0)
                                px[r, c] = 0
        max_number_blocks = (image.get_img_height()/max_length)*(image.get_img_width()/max_width)
        number_blocks = len(image.get_blocks())
        if (number_blocks >= 0.8*max_number_blocks):
            image.clear_blocks()
        ###################
        ## image is ready
        ###################
        px = None
        main_line = image.get_main_line()

        socketIO.wait(0.001)
        routing = True

        if routing == False:
            go_first_block(70, main_line)
        stop = time.time()
        #print "Command verstuurd na ", stop - start, " seconden."
        if len(beeldverwerkingNameSpace.current_route_description) > 0 and beeldverwerkingNameSpace.is_started and routing == True:
            print beeldverwerkingNameSpace.current_route_description
            print main_line
            command = beeldverwerkingNameSpace.current_route_description[0]
            name = command["commandName"]
            if name == "right":
                blocks_right = image.get_blocks_right_of_line(main_line)
                if is_crossing(main_line, blocks_right):
                    if last_street > 5:
                        street_counter += 1
                    last_street = 0
                else:
                    last_street += 1

                if street_counter >= int(command["params"]["nr"]):
                    street_counter = 0
                    beeldverwerking_namespace.finish_command(command["id"])
                else:
                    go_first_block(70, main_line)

            elif name == "left":
                blocks_left = image.get_blocks_left_of_line(main_line)
                if is_crossing(main_line, blocks_left):
                    if not last_street > 5:
                        street_counter += 1
                    last_street = 0
                else:
                    last_street += 1

                if street_counter >= int(command["params"]["nr"]):
                    street_counter = 0
                    beeldverwerking_namespace.finish_command(command["id"])
                else:
                    go_first_block(70, main_line)

            elif name == "stop":
                blocks_left = image.get_blocks_left_of_line(main_line)
                blocks_right = image.get_blocks_right_of_line(main_line)
                if (is_crossing(main_line, blocks_right) or is_crossing(main_line, blocks_left)):
                    if last_street > 5:
                        street_counter += 1
                    last_street = 0
                else:
                    last_street += 1

                if street_counter >= int(command["params"]["nr"]):
                    print "done----------------------------------------------------------------------------------\n--------------------------------------------------------"
                    street_counter = 0
                    beeldverwerking_namespace.finish_command(command["id"])
                else:
                    go_first_block(70, main_line)
            elif name == "start":
                beeldverwerking_namespace.finish_command(command["id"])  # TODO: moet dit wel?
            else:
                print "unsupported action!!!!!!!!!!!"
            print street_counter
        else:
            last_street += 1
            street_counter = 0

        #########else:
            ################print beeldverwerkingNameSpace.current_route_description
        ##############
        ## visual
        #############

        for t in image.get_blocks():
            location = t.get_middle()
            pxbackup[location[1]][location[0]] = 150

        pxbackup = cv.cvtColor(pxbackup, cv.COLOR_GRAY2RGB)

        # pxres = cv.resize(pxbackup, (img_width, img_height), interpolation=cv.INTER_NEAREST)
        img_width1 = pxbackup.shape[1]
        img_height1 = pxbackup.shape[0]

        width_ratio = (bw_width/4)/float(img_width1)
        height_ratio = (bw_height/4)/float(img_height1)



        foto = cv.resize(pxbackup, (bw_width/4, bw_height/4), interpolation=cv.INTER_NEAREST)
        try:
            for t in image.get_main_line().get_blocks():
                index = image.get_main_line().get_blocks().index(t)-1
               # print index
                if index != -1:
                    cv.line(foto,(int(math.ceil(t.get_middle()[0]*width_ratio + width_ratio/2)), int(math.ceil(t.get_middle()[1]* height_ratio + height_ratio/2))),
                            (int(math.ceil(image.get_main_line().get_blocks()[index].get_middle()[0] * width_ratio + width_ratio/2)),
                             int(math.ceil(image.get_main_line().get_blocks()[index].get_middle()[1] * height_ratio + height_ratio/2))),
                            [0,0,255])
        except ValueError:
            pass
        pxbackup = None

        cv.imshow('Result', foto)
        cv.imshow('oorspr', frame)

        #cv.imshow('Result', pxbackup)

        # cv.resize(pxres, (pxres.shape[1] / 2, pxres.shape[0] / 2),interpolation=cv.INTER_NEAREST)

        if cv.waitKey(1) == 27:
            exit(0)




    """
        # Image showing
        show_original = 1
        show_bw = 2
        show_cut1 = 3
        show_cut2 = 4
        show_result = 5
        show_x = 5

        if show_x is show_original:
            cv.imshow('Result', cv.resize(frame, (frame.shape[1] / 4, frame.shape[0] / 4), interpolation=cv.INTER_NEAREST))
            cv.waitKey(0)
        elif show_x is show_bw:
            cv.imshow('Result', cv.resize(bw, (bw.shape[1] / 4, bw.shape[0] / 4), interpolation=cv.INTER_NEAREST))
            cv.waitKey(0)
        elif show_x is show_cut1:
            cv.imshow('Result', cv.resize(cut1, (cut1.shape[1] / 4, cut1.shape[0] / 2), interpolation=cv.INTER_NEAREST))
            cv.waitKey(0)
        elif show_x is show_cut2:
            cv.imshow('Result', cv.resize(cut2, (cut2.shape[1] / 2, cut2.shape[0] / 2), interpolation=cv.INTER_NEAREST))
            cv.waitKey(0)
        elif show_x is show_result:
            cv.imshow('Result', cv.resize(pxres, (pxres.shape[1] / 2, pxres.shape[0] / 2), interpolation=cv.INTER_NEAREST))
            cv.waitKey(0)
    """
        ##########################
        ## hier bebingt de stuur logica
        ##########################
