# -*- coding: utf-8 -*-
#
# @Project : MMK3-HID-Control
# @File	   : message.py
# @Date    : 2020-05-03 20:25:37
# @Author  : Emerah (MaXaR) - ahmed.emerah@icloud.com
# @Link    : https://github.com/Emerah
# @Version : 1.0.0
#
# *****************************************************************************


class MessageBase(object):

    @property
    def byte_value(self):
        raise NotImplementedError

    def _converted(self, value: int, byte_length=1):
        new_value = value.to_bytes(byte_length, 'big')
        return new_value


class Header(MessageBase):

    def __init__(self, screen_index: int):
        assert screen_index in range(2)
        super().__init__()
        self._screen_index = self._converted(screen_index)

    @property
    def screen_index(self):
        return self._screen_index

    @screen_index.setter
    def screen_index(self, new_value):
        assert new_value in range(2)
        self._screen_index = self._converted(new_value)

    @property
    def byte_value(self):
        return bytes.fromhex('8400') + self._screen_index + bytes.fromhex('60') + bytes.fromhex('00000000')


class Coordinates(MessageBase):

    def __init__(self, x_pos: int, y_pos: int):
        assert x_pos in range(480)
        assert y_pos in range(272)
        super().__init__()
        self._x_pos = self._converted(x_pos, byte_length=2)
        self._y_pos = self._converted(y_pos, byte_length=2)

    @property
    def x_position(self):
        return self._x_pos

    @x_position.setter
    def x_position(self, new_value):
        assert new_value in range(480)
        self._x_pos = self._converted(new_value, byte_length=2)

    @property
    def y_position(self):
        return self._y_pos

    @y_position.setter
    def y_position(self, new_value):
        assert new_value in range(272)
        self._y_pos = self._converted(new_value, byte_length=2)

    @property
    def byte_value(self):
        return self._x_pos + self._y_pos


class Size(MessageBase):

    def __init__(self, width: int, height: int):
        assert width > 0 and width <= 480
        assert height > 0 and height <= 272
        super().__init__()
        self._width = self._converted(width, byte_length=2)
        self._height = self._converted(height, byte_length=2)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, new_value):
        assert new_value > 0 and new_value <= 480
        self._width = self._converted(new_value, byte_length=2)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new_value):
        assert new_value > 0 and new_value <= 272
        self._height = self._converted(new_value, byte_length=2)

    @property
    def byte_value(self):
        return self._width + self._height


class Command(MessageBase):
    pass


class Repeat(Command):

    def __init__(self, repeat_count):
        assert repeat_count > 0 and repeat_count <= 65280  # screen width * screen height / 2
        super().__init__()
        self._repeat_count = self._converted(repeat_count, byte_length=2)

    @property
    def repeat_count(self):
        return self._repeat_count

    @repeat_count.setter
    def repeat_count(self, new_value):
        self._repeat_count = self._converted(new_value, 2)

    @property
    def byte_value(self):
        return bytes.fromhex('0100') + self._repeat_count


class Transfer(Command):

    def __init__(self, num_pixel_pairs: int):
        super().__init__()
        self._num_pixel_pais = self._converted(num_pixel_pairs, byte_length=2)

    @property
    def num_pixel_pairs(self):
        return self._num_pixel_pais

    @property
    def byte_value(self):
        return bytes.fromhex('0000') + self.num_pixel_pairs


class Skip(Command):

    def __init__(self, args):
        super().__init__(command=2, args=args)

    @property
    def byte_value(self):
        return


class Blit(MessageBase):

    @property
    def byte_value(self):
        return bytes.fromhex('03000000')


class End(Header):

    @property
    def byte_value(self):
        return bytes.fromhex('4000') + self._screen_index + bytes.fromhex('00')


class ColorPixel(MessageBase):

    def __init__(self, value):
        assert value <= 65536  # maximum number a 16-word number can hold (256*256)
        super().__init__()
        self._value = self._converted(value, byte_length=2)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        assert new_value <= 65536
        self._value = self._converted(new_value, 2)

    @property
    def byte_value(self):
        return self.value


class ColorMessage(MessageBase):
    def __init__(self, header: Header, coordinates: Coordinates, size: Size, command: Command, data: ColorPixel, blit: Blit, end: End):
        # def __init__(self, header, coordinates, size, command, data, blit, end):
        super().__init__()
        self._header = header
        self._coordinates = coordinates
        self._size = size
        self._command = command
        self._data = data
        self._blit = blit
        self._end = end

    @property
    def header(self):
        return self._header.byte_value

    @property
    def coordinates(self):
        return self._coordinates.byte_value

    @property
    def size(self):
        return self._size.byte_value

    @property
    def command(self):
        return self._command.byte_value

    @property
    def data(self):
        return self._data.byte_value + self._data.byte_value

    @property
    def blit(self):
        return self._blit.byte_value

    @property
    def end(self):
        return self._end.byte_value

    @property
    def byte_value(self):
        return self.header + self.coordinates + self.size + self.command + self.data + self.blit + self.end


class ImageMessage(MessageBase):
    def __init__(self, header: Header, coordinates: Coordinates, size: Size, command: Command, data: bytes, blit: Blit, end: End):
        self._header = header
        self._coordinates = coordinates
        self._size = size
        self._command = command
        self._data = data
        self._blit = blit
        self._end = end

    @property
    def byte_value(self):
        return self._header.byte_value + self._coordinates.byte_value + self._size.byte_value + self._command + self._data + self._blit.byte_value + self._end.byte_value
