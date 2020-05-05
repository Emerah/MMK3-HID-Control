# -*- coding: utf-8 -*-
#
# @Project : MMK3-HID-Control
# @File	   : image.py
# @Date    : 2020-05-04 02:02:30
# @Author  : Emerah (MaXaR) - ahmed.emerah@icloud.com
# @Link    : https://github.com/Emerah
# @Version : 1.0.0
#
# *****************************************************************************


# from PyQt5.QtGui import QImage
# from PyQt5.QtCore import QByteArray
from rgb_pixel import RGBPixel
from PIL import Image
from functools import reduce
from operator import add


class MaschineImage(object):

    def __init__(self, image_name):
        self._image_name = image_name
        super().__init__()
        image = Image.open(image_name)
        image = image.resize((480, 272))
        self._image = image

    @property
    def image(self):
        return self._image

    @property
    def rgb888_pixels(self):
        return list(self._get_image_pixels())

    @property
    def rgb565_bytes(self):
        return self._pixels_to_bytes()

    def _converted(self, pixel):
        return RGBPixel(pixel_value=pixel).byte_value

    def _get_image_pixels(self):
        return self._image.getdata()

    def _pixels_to_bytes(self):
        data = []
        for pixel in list(self._get_image_pixels()):
            converted = self._converted(pixel)
            data.append(converted)
        data = reduce(add, data)
        return data


# image = MaschineImage('Live.jpg')
# image_bytes = image.rgb565_bytes

# print(len(image_bytes))
# print('done')
