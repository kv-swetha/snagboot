import usb
import logging
logger = logging.getLogger("snagrecover")
from snagrecover.firmware.firmware import run_firmware
from snagrecover.utils import get_usb,parse_usb
from snagrecover.config import recovery_config
import time
import threading

def run_tiboot3(dev):
	run_firmware(dev, "tiboot3")

def run_uboot(dev):
	run_firmware(dev, "u-boot")
	run_firmware(dev, "tispl")


def main():
	usb_vid = recovery_config["rom_usb"][0]
	usb_pid = recovery_config["rom_usb"][1]

	get_usb(usb_vid,usb_pid)
	devices = find_usb(usb_vid,usb_pid)
	list_thread = []

	for dev in devices:
		print(dev)
		t1 = threading.Thread(target=run_tiboot3, args=(dev,))
		t1.start()
		list_thread.append(t1)

	for thread in list_thread:	
		thread.join()

	list_thread.clear()

	# USB device should re-enumerate at this point
	for dev in devices:
		usb.util.dispose_resources(dev)

	# without this delay, USB device will be present but not ready
	time.sleep(1)

	get_usb(usb_vid,usb_pid)
	devices_new = find_usb(usb_vid,usb_pid)

	for dev in devices_new:
		if "usb" in recovery_config["firmware"]["tiboot3"]:
			(usb_vid,usb_pid) = parse_usb(recovery_config["firmware"]["tiboot3"]["usb"])
		print(dev)
		t1 = threading.Thread(target=run_uboot, args=(dev,))
		t1.start()
		list_thread.append(t1)

	for thread in list_thread:	
		thread.join()	

	list_thread.clear()

