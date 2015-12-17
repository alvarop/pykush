#!/usr/bin/env python
''' Python interface for Yepkit's YKUSH usb hub

    Currently tested and working on Ubuntu.
'''

import usb.core
import usb.util


class PYKUSH(object):

    __VENDOR_ID = 0x04D8
    __PRODUCT_ID = 0xF2F7
    __OLD_PRODUCT_ID = 0x0042

    def __init__(self, serial_number=None):
        self.serial_number = serial_number

        self.dev = usb.core.find(
            idVendor=self.__VENDOR_ID, idProduct=self.__PRODUCT_ID)

        if self.dev is None:
            raise ValueError('YKUSH not found')

        # Detach kernel driver if possible
        try:
            self.dev.detach_kernel_driver(0)
        except usb.core.USBError:
            # Must already be detached
            pass

        self.dev.set_configuration()

        # get an endpoint instance
        cfg = self.dev.get_active_configuration()
        intf = cfg[(0, 0)]

        if self.dev.serial_number:
            self.serial_number = str(self.dev.serial_number)
        else:
            self.serial_number = None

        self.ep = usb.util.find_descriptor(
            intf,
            # match the first OUT endpoint
            custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)

        assert self.ep is not None

    def send_command(self, command):
        out_buff = [0] * 64
        out_buff[0] = command

        self.ep.write(out_buff, timeout=5000)
        in_buff = self.ep.read(64, timeout=120000)
        # TODO - something with return value...

    def enable_all(self):
        self.send_command(0x1a)

    def disable_all(self):
        self.send_command(0x0a)

    def enable(self, port):
        if port < 1 or port > 3:
            raise ValueError('Invalid port. Supported ports are: 1,2, and 3')

        cmd = 0x10 | port
        self.send_command(cmd)

    def disable(self, port):
        if port < 1 or port > 3:
            raise ValueError('Invalid port. Supported ports are: 1,2, and 3')

        cmd = 0x00 | port
        self.send_command(cmd)
