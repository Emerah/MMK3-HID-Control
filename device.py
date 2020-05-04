# -*- coding: utf-8 -*-
#
# @Project : MMK3-HID-Control
# @File	   : device.py
# @Date    : 2020-05-01 14:42:19
# @Author  : Emerah (MaXaR) - ahmed.emerah@icloud.com
# @Link    : https://github.com/Emerah
# @Version : 1.0.0
#
# *****************************************************************************


import usb

NATIVE_INSTRUMENTS_ID = 0x17cc
MASCHINE_MKIII_ID = 0x1600


class MaschineMKiii(object):

    def __init__(self):
        self.__maschine_handle = None
        self.__bulk_interface = None
        self.__bulk_endpoint = None
        super().__init__()
        self.__do_setup()

    @property
    def maschine_handle(self):
        return self.__maschine_handle

    @property
    def bulk_transfer_interface(self):
        return self.__bulk_interface

    @property
    def bulk_transfer_endpoint(self):
        return self.__bulk_endpoint

    def claim_bulk_interface(self):
        self.__claim__interface(self.__bulk_interface)

    def release_bulk_interface(self):
        self.__release_interface(self.__bulk_interface)

    def send_bulk_transfer_data(self, data):
        self.__maschine_handle.write(self.__bulk_endpoint, data)

    def dispose(self):
        usb.util.dispose_resources(self.__maschine_handle)

    # @property
    # def hid_interface(self):
    #     return self.__hid_interface

    # @property
    # def midi_interface(self):
    #     return self.__midi_interface

    # @property
    # def midi_endpoint(self):
    #     return self.__midi_endpoint

    # @property
    # def hid_endpoint(self):
    #     return self.__hid_endpoint

    def __do_setup(self):
        # get a handle on the maschine device
        maschine = usb.core.find(idVendor=NATIVE_INSTRUMENTS_ID, idProduct=MASCHINE_MKIII_ID)
        assert maschine is not None
        # we must activate the device configuration
        maschine.set_configuration()
        self.__maschine_handle = maschine
        # get the current configuration
        config = maschine.get_active_configuration()
        # get the bulk interface from maschine configuration (5 for maschine)
        bulk_interface = config[(5, 0)]
        assert bulk_interface is not None
        self.__bulk_interface = bulk_interface
        # get the bulk endpoint, this is the endpoint we send data to.
        bulk_endpoint = usb.util.find_descriptor(bulk_interface, custom_match=lambda ep: ep.bEndpointAddress == 4)
        assert bulk_endpoint is not None
        self.__bulk_endpoint = bulk_endpoint

    def __claim__interface(self, interface):
        usb.util.claim_interface(self.__maschine_handle, interface)

    def __release_interface(self, interface):
        usb.util.release_interface(self.__maschine_handle, interface)
