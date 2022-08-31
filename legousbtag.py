#!/usr/bin/python

import usb
import util

# UIDs can be retrieved with Android App (most probably in hexadecimal)
uidDarthVader = (4, 161, 158, 210, 227, 64, 128) # Darth Vader from Disney Infinity 3.0


def uid_compare(uid1, uid2):
    match = True
    for i in range(0, 7):
        if uid1[i] != uid2[i]:
            match = False
    return match 


def main():
    device = util.init_usb()
    pad_in_center = False
    if device is not None:
        while not pad_in_center:
            try:
                in_packet = device.read(0x81, 32, timeout=10)
                bytelist = list(in_packet)

                if not bytelist:
                    pass
                elif bytelist[0] != 0x56:  # NFC packets start with 0x56
                    pass
                else:
                    pad_num = bytelist[2]
                    uid_bytes = bytelist[6:13]
                    match = uid_compare(uid_bytes, uidDarthVader)
                    action = bytelist[5]

                    # Tag inserted
                    if action == util.ACTIONS['inserted']:
                        print('Tag inserted on pad ', pad_num)
                        if match:
                            # Darth Vader
                            util.switch_pad(device, pad_num, util.COLORS['red'])
                        else:
                            # some other tag
                            util.switch_pad(device, pad_num, util.COLORS['green'])

                        if pad_num == util.PADS_ID['center']:
                            pad_in_center = True

                    # Tag removed
                    else:
                        util.switch_pad(device, pad_num, util.OFF)
                        print('Tag removed from pad ', pad_num)

            except usb.USBError as err:
                # print("Encountered USB error ! ", err)
                pass

        # Switch off
        util.switch_pad(device, util.PADS_ID['all'], util.OFF)
    return


if __name__ == '__main__':
    main()
