import sys
import usb.core
import usb.util

# Seems to be the 'wake up' signal
TOYPAD_INIT = [0x55, 0x0f, 0xb0, 0x01,
               0x28, 0x63, 0x29, 0x20,
               0x4c, 0x45, 0x47, 0x4f,
               0x20, 0x32, 0x30, 0x31,
               0x34, 0xf7, 0x00, 0x00,
               0x00, 0x00, 0x00, 0x00,
               0x00, 0x00, 0x00, 0x00,
               0x00, 0x00, 0x00, 0x00]

# RESPONSE = 0x55
# Event = 0x56

# Colors
OFF = [0, 0, 0]
COLORS = {
    'red': [255, 0, 0],
    'green': [0, 255, 0],
    'blue': [0, 0, 255],
    'purple': [255, 0, 255],
    'cyan': [0, 255, 255],
    'lgreen': [255, 255, 0],
    'white': [255, 255, 255],
    'dgreen': [40, 128, 0],
    'dblue': [0, 40, 128],
    'pink': [128, 0, 40],
    'lblue': [56, 128, 56],
}

# Pads ID
PADS_ID = {
    'all': 0,
    'center': 1,
    'left': 2,
    'right': 3,
}

# Actions
ACTIONS = {
    'inserted': 0,
    'removed': 1,
}


def init_usb():

    dev = usb.core.find(idVendor=0x0e6f, idProduct=0x0241)

    if dev is None:
        print('Device not found')
    else:
        if not sys.platform.startswith('win'):
            if dev.is_kernel_driver_active(0):
                dev.detach_kernel_driver(0)

        print(usb.util.get_string(dev, dev.iProduct))

        dev.set_configuration()
        dev.write(1, TOYPAD_INIT)

    return dev


def send_command(dev, command):

    # calculate checksum
    checksum = 0
    for word in command:
        checksum = checksum + word
        if checksum >= 256:
            checksum -= 256
    message = command+[checksum]

    # pad message
    while len(message) < 32:
        message.append(0x00)

    # send message
    dev.write(1, message)

    return


def switch_pad(dev, pad, colour):
    send_command(dev, [0x55, 0x06, 0xc0, 0x02, pad, colour[0], colour[1], colour[2], ])
    return
