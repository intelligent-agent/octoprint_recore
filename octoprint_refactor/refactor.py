
BOOTDEVICE_USB  = "extraargs=root=/dev/sda1"
BOOTDEVICE_EMMC = "extraargs=root=/dev/mmcblk0p1"
BOOT_ARGS_FILE = "/boot/armbianEnv.txt"

import os.path

class Refactor:
    def __init__(self, settings):
        self.refactor_version_file = settings.get(["version_file"])
        self.klipper_dir = settings.get(["klipper_dir"])
        if self.get_rootfs() == "emmc":
            self.boot_args_file_path = BOOT_ARGS_FILE
        else:
            self.boot_args_file_path = "/mnt"+BOOT_ARGS_FILE

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
        for line in open(self.boot_args_file_path, 'r'):
            if re.search('extraargs', line):
                if BOOTDEVICE_USB in line:
                    return "usb"
        return "emmc"

    def change_boot_media(self):
        if self.get_boot_media() == "emmc":
            self.set_boot_media(BOOTDEVICE_USB)
        else:
            self.set_boot_media(BOOTDEVICE_EMMC)

    def set_boot_media(self, new_boot_device):
        self.remove_boot_media()
        with open(self.boot_args_file_path, 'a') as f:
            f.write(new_boot_device+"\n")

    def remove_boot_media(self):
        with open(self.boot_args_file_path,"r+") as f:
            new_f = f.readlines()
            f.seek(0)
            for line in new_f:
                if "extraargs" not in line:
                    f.write(line)
            f.truncate()

    def is_usb_present(self):
        if self.get_rootfs() == "usb":
            return True
        return os.path.isfile("/mnt"+BOOT_ARGS_FILE)

    def is_emmc_present(self):
        if self.get_rootfs() == "emmc":
            return True
        return os.path.isfile("/mnt"+BOOT_ARGS_FILE)
