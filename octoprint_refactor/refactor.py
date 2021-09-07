
BOOTDEVICE_USB  = "extraargs=root=/dev/sda1"
BOOTDEVICE_EMMC = "extraargs=root=/dev/mmcblk0p1"
BOOT_ARGS_FILE = "/boot/armbianEnv.txt"
EMMC_BOOT_ARGS_FILE = "/mnt/emmc/"+BOOT_ARGS_FILE
USB_BOOT_ARGS_FILE = "/mnt/usb/"+BOOT_ARGS_FILE

import os.path

class Refactor:
    def __init__(self, settings):
        self.refactor_version_file = settings.get(["version_file"])
        self.klipper_dir = settings.get(["klipper_dir"])

    def get_refactor_version(self):
        with open(self.refactor_version_file, "r") as f:
            version = f.read().replace("\n", "")
            return version

    def get_klipper_version(self):
        import subprocess
        path = "git -C "+self.klipper_dir+" describe --always --tags --long --dirty"
        try:
            return subprocess.check_output(path.split()).strip()
        except subprocess.CalledProcessError:
            return "Unknown"

    def get_rootfs(self):
        import re
        for line in open("/proc/mounts", 'r'):
            if re.search('/ ', line):
                if "mmcblk" in line:
                    return "emmc"
                elif "sd" in line:
                    return "usb"
                elif "nvme" in line:
                    return "usb"
                else:
                    return line
                if line == None:
                    return 'Unknown'

    def get_boot_media(self):
        import re
        for line in open(EMMC_BOOT_ARGS_FILE, 'r'):
            if re.search('extraargs', line):
                if BOOTDEVICE_USB in line:
                    return "usb"
                elif BOOTDEVICE_EMMC in line:
                    return "emmc"
        return "emmc"

    def change_boot_media(self):
        if self.get_boot_media() == "emmc":
            os.system("sudo /sbin/set-boot-media usb")
        else:
            os.system("sudo /sbin/set-boot-media emmc")

    def is_usb_present(self):
        if self.get_rootfs() == "usb":
            return True
        return os.path.isfile(USB_BOOT_ARGS_FILE)

    def is_emmc_present(self):
        if self.get_rootfs() == "emmc":
            return True
        return os.path.isfile(EMMC_BOOT_ARGS_FILE)
