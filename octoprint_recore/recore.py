import os.path
import concurrent.futures
import subprocess
import time


class Recore:
    def __init__(self, settings):
        self.recore_version_file = settings.get(["version_file"])
        self.klipper_dir = settings.get(["klipper_dir"])

    def get_recore_version(self):
        with open(self.recore_version_file, "r") as f:
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

    def set_ssh_enabled(self, enabled):
        is_enabled = "true" if enabled else "false"
        os.system(f"sudo /usr/local/bin/set-ssh-access {is_enabled}")

    def is_ssh_enabled():
        return Recore.run_system_command("/usr/local/bin/is-ssh-enabled") == "true"
