import usb

def find_usb(vid: int, pid: int):

    dev = usb.core.find(idVendor=vid, idProduct=pid,find_all=1)
    return dev