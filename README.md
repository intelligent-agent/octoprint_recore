# OctoPrint-Refactor

This plugin has been custom made to work with Refactor distribution and allows
users to install updated versions of the software.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/intelligent-agent/octoprint_refactor/archive/main.zip

The plugin should come preinstalled with Refactor v3.0.2 and later,
but for earlier versions of Refactor, it must be installed manually through the
OctoPrint web interface.

Because there are some settings that need root access to start, users that
are on earlier Refactor versions must run a "bootstrap" script in order to get set up.
This requires access to the command line.

## Configuration

**TODO:** Describe your plugin's configuration options (if any).

TODO:
automatically mount /dev/mmcblk0p1 on /mnt/ if booting from USB
automatically mount /dev/sda1 on /mnt/ if booting from eMMC

give debian sudo access to /sbin/set-boot-media
