#!/usr/bin/python

# A python script to cycle all available colors the Lego USB Pad can create.
import util
from time import sleep
from random import choices


def test_all_colors(device):
    """
    Test all colors on all pads
    """

    for curr_key, curr_color in util.COLORS.items():
        print(curr_key)
        util.switch_pad(device, util.PADS_ID['all'], curr_color)
        sleep(1.5)


def pulse(device, pad, color, bpm=120):
    """

    :param device:
    :param pad:
    :param color:
    :param bpm:
    """

    # Compute sleep time: need to divide by two so we can switch the pad on and off
    sleep_time = 30/bpm

    util.switch_pad(device, util.PADS_ID[pad], util.COLORS[color])
    sleep(sleep_time)

    util.switch_pad(device, util.PADS_ID[pad], util.OFF)
    sleep(sleep_time)


def random_pulse(device, bpm=120):
    """

    :param device:
    :param bpm:
    """

    # Compute sleep time
    sleep_time = 60/bpm

    # Pick a random color for each pad
    curr_colors = choices(list(util.COLORS.values()), k=3)

    util.switch_pad(device, 1, curr_colors[0])
    util.switch_pad(device, 2, curr_colors[1])
    util.switch_pad(device, 3, curr_colors[2])
    sleep(sleep_time)


def up_and_down(device, pad, color):
    """

    :param device:
    :param pad:
    :param color:
    """
    iterations = 10

    # define lists of 10 values for each color component, starting from their max
    r_range = [util.COLORS[color][0]-i*int(util.COLORS[color][0]/iterations) for i in range(1, iterations+1)]
    g_range = [util.COLORS[color][1]-i*int(util.COLORS[color][1]/iterations) for i in range(1, iterations+1)]
    b_range = [util.COLORS[color][2]-i*int(util.COLORS[color][2]/iterations) for i in range(1, iterations+1)]

    # Do it twice so it goes up then down
    for it in range(iterations).__reversed__():
        util.switch_pad(device, util.PADS_ID[pad], [r_range[it], g_range[it], b_range[it]])
        sleep(0.05)
    for it in range(iterations):
        util.switch_pad(device, util.PADS_ID[pad], [r_range[it], g_range[it], b_range[it]])
        sleep(0.05)


def main():
    # Init pad communication
    device = util.init_usb()

    # Test all colors on all pads
    test_all_colors(device)

    # 30s pulse using default params
    for it in range(30):
        pulse(device, 'all', 'dgreen')

    # 30s random pulse at 180bpm
    for it in range(30):
        random_pulse(device, bpm=180)

    # color graduation on center pad
    up_and_down(device, "center", "pink")

    # Switch off
    util.switch_pad(device, util.PADS_ID['all'], util.OFF)


if __name__ == '__main__':
    main()
