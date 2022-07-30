import os.path
import concurrent.futures
import subprocess
import time


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
        path = "git -C " + self.klipper_dir + " describe --always --tags --long --dirty"
        try:
            return subprocess.check_output(path.split()).strip()
        except subprocess.CalledProcessError:
            return "Unknown"

    def run_system_command(command):
        return subprocess.run(command.split(),
                              capture_output=True,
                              text=True).stdout.strip()

    def get_rootfs():
        return Refactor.run_system_command("/usr/local/bin/get-rootfs")

    def get_boot_media(self):
        return Refactor.run_system_command("sudo /usr/local/bin/get-boot-media")

    def change_boot_media(self):
        if self.get_boot_media() == "emmc":
            os.system("sudo /usr/local/bin/set-boot-media usb")
        else:
            os.system("sudo /usr/local/bin/set-boot-media emmc")

    def set_ssh_enabled(self, enabled):
        is_enabled = "true" if enabled else "false"
        os.system(f"sudo /usr/local/bin/set-ssh-access {is_enabled}")

    def is_usb_present():
        return Refactor.run_system_command("/usr/local/bin/is-media-present usb") == "yes"

    def is_emmc_present():
        return Refactor.run_system_command("/usr/local/bin/is-media-present emmc") == "yes"

    def is_ssh_enabled():
        return Refactor.run_system_command("/usr/local/bin/is-ssh-enabled") == "yes"
