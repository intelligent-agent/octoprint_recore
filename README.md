# OctoPrint-Refactor

This plugin has been custom made to work with Refactor distribution and allows
users to install updated versions of the software.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/intelligent-agent/octoprint_refactor/archive/main.zip

The plugin should come preinstalled with Refactor v3.0.2 and later.

Because there are some settings that need root access to start, users that
are on earlier Refactor versions must run a "bootstrap" script in order to get set up.
This requires access to the command line using ssh.

From the commandline:
    wget https://raw.githubusercontent.com/intelligent-agent/octoprint_refactor/main/bins/migrate-from-v301-to-v302-set-rootdev.sh
    bash migrate-from-v301-to-v302-set-rootdev.sh

This bash script will check for the presence of a Refactor image on the (only) USB drive inserted
in the printer. It will then go on to do an fsck to make sure the integrity of the image is OK.
Finally, the script will update the file /boot/armbianEnv.txt and set the rootdev
to partition 2 of the USB drive.

Once the script finishes, the user is asked to reboot.
There is a caveat here. Since the kernel installed on the eMMC drive is
different than the kernel on the root file system, the nftables service will
not run, so the user must use the right port (5000) in order to access the
web interface. The address for OctoPrint then becomes: recore.local:5000

Once the user interface is loaded, revision v3.0.2-RC4 can be downloaded and the finally flashed.
