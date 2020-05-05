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

import random
import time

from device import MaschineMKiii
from image import MaschineImage
from message import (Blit, ColorMessage, ColorPixel, Coordinates, End, Header, Repeat, Size, ImageMessage)  # Transfer
from util import suspend_ni_backend_support


def do_screen_color_test():
    header = Header(screen_index=0)
    coordinates = Coordinates(x_pos=0, y_pos=0)
    size = Size(width=480, height=272)
    command = Repeat(int(480*272/2))
    data = ColorPixel(value=43594)
    blit = Blit()
    end = End(screen_index=0)
    message = ColorMessage(header=header, coordinates=coordinates, size=size, command=command, data=data, blit=blit, end=end)
    maschine.claim_bulk_interface()
    for i in range(5):
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


def do_image_test():
    live_image = MaschineImage('Live.jpg')
    live_image_bytes = live_image.rgb565_bytes
    maschine_image = MaschineImage('maschine.jpg')
    maschine_image_bytes = maschine_image.rgb565_bytes
    header = Header(screen_index=0)
    coordinates = Coordinates(x_pos=0, y_pos=0)
    size = Size(width=480, height=272)
    # command = Transfer(int(len(live_image_bytes) / 2))
    command = bytes.fromhex('0000ff00')
    data = live_image_bytes
    blit = Blit()
    end = End(screen_index=0)
    live_message = ImageMessage(header=header, coordinates=coordinates, size=size, command=command, data=data, blit=blit, end=end)
    maschine.claim_bulk_interface()
    maschine.send_bulk_transfer_data(live_message.byte_value)
    header.screen_index = 1
    data = maschine_image_bytes
    end.screen_index = 1
    maschine_message = ImageMessage(header=header, coordinates=coordinates, size=size, command=command, data=data, blit=blit, end=end)
    maschine.send_bulk_transfer_data(maschine_message.byte_value)
    maschine.release_bulk_interface()


if __name__ == "__main__":
    running = False
    if running:
        suspend_ni_backend_support()
    maschine = MaschineMKiii()
    do_screen_color_test()
    do_image_test()
    maschine.dispose()
    print('done')
