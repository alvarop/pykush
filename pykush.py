#!/usr/bin/env python
''' Python interface for Yepkit's YKUSH usb hub '''

import usb.core
import usb.util

VENDOR_ID = 0x04D8
PRODUCT_ID = 0xF2F7
OLD_PRODUCT_ID = 0x0042

dev = usb.core.find(idVendor=VENDOR_ID, idProduct=0xF2F7)

if dev is None:
    raise ValueError('Device not found')

print('Device Connected!')

dev.set_configuration(1)

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

dev.detach_kernel_driver(intf)

print('Serial Number: ' + str(dev.serial_number))

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

cmd = 0x1a  # All downstream ports UP

out_buff = [0] * 64
out_buff[0] = cmd

print('Attempting Write')
# write the data
ep.write(out_buff, timeout=5000)

print('Attempting Read')
in_buff = ep.read(64, timeout=120000)

print(in_buff)

dev.attach_kernel_driver(intf)