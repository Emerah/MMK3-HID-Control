# -*- coding: utf-8 -*-
#
# @Project : MMK3-HID-Control
# @File	   : pixel_conversion.py
# @Date    : 2020-05-05 17:45:30
# @Author  : Emerah (MaXaR) - ahmed.emerah@icloud.com
# @Link    : https://github.com/Emerah
# @Version : 1.0.0
#
# *****************************************************************************


class RGBPixel(object):

    def __init__(self, pixel_value: tuple):
        assert len(pixel_value) == 3
        self._pixel_value = pixel_value

    def _convert_rgb888_to_rgb565(self, pixel_value):
        rgb565 = 0
        b_r = (pixel_value[0] * 249 + 1014) >> 11
        b_g = (pixel_value[1] * 253 + 505) >> 10
        b_b = (pixel_value[2] * 249 + 1014) >> 11
        rgb565 = rgb565 | (b_r << 11)
        rgb565 = rgb565 | (b_g << 5)
        rgb565 = rgb565 | b_b
        b_val = rgb565.to_bytes(2, 'big')
        return b_val

    @property
    def byte_value(self):
        return self._convert_rgb888_to_rgb565(self._pixel_value)
