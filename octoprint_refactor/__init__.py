# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import flask
from .refactor import Refactor

class RefactorPlugin(octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.SimpleApiPlugin
):

    def on_after_startup(self):
        settings = self._settings
        self.refactor = Refactor(settings)
        self._logger.info("Refactor plugin!")


    def get_settings_defaults(self):
        return {
            "version_file": "/etc/refactor.version",
            "klipper_dir": "/home/debian/klipper",
            "install_script": "/root/install_refactor.sh"
        }

    def get_template_configs(self):
        return [
        ]

    def get_template_vars(self):
        return {
            "rootfs": self.refactor.get_rootfs(),
            "next_rootfs": self.refactor.get_boot_media(),
            "usb_present": self.refactor.is_usb_present(),
            "emmc_present": self.refactor.is_emmc_present()
        }

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/refactor.js"],
            "css": ["css/refactor.css"],
            "less": ["less/refactor.less"]
        }

    def get_api_commands(self):
        return dict(
            get_data=[],
            change_boot_media=[],
            install_refactor=[],
            get_install_progress=[]
        )

    def on_api_command(self, command, data):
        import flask
        if command == "get_data":
            data = {
                "versions": {
                    "refactor": {
                        "name": "Refactor",
                        "version": self.refactor.get_refactor_version()
                    },
                    "klipper": {
                        "name": "Klipper",
                        "version": self.refactor.get_klipper_version()
                    }
                },
                "boot_media": self.refactor.get_boot_media()
            }
            return flask.jsonify(**data)
        elif command == "change_boot_media":
            self.refactor.change_boot_media()
            status = {
                "boot_media": self.refactor.get_boot_media()
            }
            return flask.jsonify(**status)
        elif command == "install_refactor":
            status = {
            }
            return flask.jsonify(**status)
        elif command == "get_install_progress":
            progress = {
            }
            return flask.jsonify(**progress)

    def on_api_get(self, request):
        return flask.jsonify(foo="bar")

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "refactor": {
                "displayName": "Refactor",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "intelligent-agent",
                "repo": "octoprint_refactor",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/intelligent-agent/octoprint_refactor/archive/{target_version}.zip",
            }
        }

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = RefactorPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
