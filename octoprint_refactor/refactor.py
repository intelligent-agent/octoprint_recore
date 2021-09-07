
BOOTDEVICE_USB  = "extraargs=root=/dev/sda1"
BOOTDEVICE_EMMC = "extraargs=root=/dev/mmcblk0p1"
BOOT_ARGS_FILE = "/boot/armbianEnv.txt"
EMMC_BOOT_ARGS_FILE = "/mnt/emmc/"+BOOT_ARGS_FILE
USB_BOOT_ARGS_FILE = "/mnt/usb/"+BOOT_ARGS_FILE

import os.path
import concurrent.futures

class Refactor:
    def __init__(self, settings):
        self.refactor_version_file = settings.get(["version_file"])
        self.klipper_dir = settings.get(["klipper_dir"])
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self.bytes_downloaded = 0
        self.bytes_to_download = 1
        self.download_cancelled = False

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

    def get_releases(self):
        import requests
        self.releases = requests.get("https://api.github.com/repos/intelligent-agent/Refactor/releases")
        return self.releases.json()

    def install_version(self, refactor_version):
        print("Downloading version: "+refactor_version["name"])
        url = refactor_version["assets"][0]['browser_download_url']
        self.bytes_downloaded = 0
        self.download_cancelled = False
        self.bytes_to_download = refactor_version["assets"][0]['size']
        self.executor.submit(self.download_refactor, url)

    def download_refactor(self, url):
        import requests
        # Answer by Dennis Patterson
        # https://stackoverflow.com/questions/53101597/how-to-download-binary-file-using-requests
        #
        local_filename = "Refactor-recore.img.xz"
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    self.bytes_downloaded += len(chunk)
                    if self.download_cancelled:
                        return

    def install_refactor(self):
        print("xz -v -d -c Refactor-recore.img.xz | dd of=/dev/mmcblk0")

    def cancel_download(self):
        self.download_cancelled = True

    def get_download_progress(self):
        return {
            "progress": (self.bytes_downloaded/self.bytes_to_download),
            "cancelled": self.download_cancelled
        }

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
