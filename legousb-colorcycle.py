#!/usr/bin/python

# A python script to cycle all available colors the Lego USB Pad can create.
import util
from time import sleep


def main():
    # Init pad communication
    device = util.init_usb()

    # Test all colors on all pads
    for curr_color in util.COLORS.values():
        sleep(0.5)
        util.switch_pad(device, util.PADS_ID['all'], curr_color)

    # Test a color graduation on center pad
    sleep(1)
    curr_color = [0, 0, 0]
    util.switch_pad(device, util.PADS_ID['all'], curr_color)
    for i in range(0, 255, 3):
        sleep(0.5)
        util.switch_pad(device, util.PADS_ID['center'], curr_color)
        curr_color[1] += 3
        print(curr_color)

    # Switch off
    sleep(1)
    print(util.COLORS)
    util.switch_pad(device, util.PADS_ID['all'], util.COLORS['off'])


if __name__ == '__main__':
    main()
