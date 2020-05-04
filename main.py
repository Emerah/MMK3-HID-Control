# -*- coding: utf-8 -*-
#
# @Project : MMK3-HID-Control
# @File	   : main.py
# @Date    : 2020-05-03 20:28:10
# @Author  : Emerah (MaXaR) - ahmed.emerah@icloud.com
# @Link    : https://github.com/Emerah
# @Version : 1.0.0
#
# *****************************************************************************

import time
import random
from message import Blit, ColorPixel, Coordinates, End, Header, Message, Repeat, Size
from util import suspend_ni_backend_support
from device import MaschineMKiii


def do_screen_color_test():
    header = Header(screen_index=0)
    coordinates = Coordinates(x_pos=0, y_pos=0)
    size = Size(width=480, height=272)
    command = Repeat(int(480*272/2))
    data = ColorPixel(value=43594)
    blit = Blit()
    end = End(screen_index=0)
    message = Message(header=header, coordinates=coordinates, size=size, command=command, data=data, blit=blit, end=end)
    maschine.claim_bulk_interface()
    for i in range(30):
        header.screen_index = 0
        color = random.choice(range(65000))
        data.value = color
        maschine.send_bulk_transfer_data(message.byte_value)
        header.screen_index = 1
        color = random.choice(range(65000))
        data.value = color
        maschine.send_bulk_transfer_data(message.byte_value)
        time.sleep(0.25)
    maschine.release_bulk_interface()
    print('full message', message.byte_value)


if __name__ == "__main__":
    running = False
    if running:
        suspend_ni_backend_support()
    maschine = MaschineMKiii()
    do_screen_color_test()
    print('done')
