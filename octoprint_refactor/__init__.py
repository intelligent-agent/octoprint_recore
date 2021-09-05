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

class RefactorPlugin(octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.SimpleApiPlugin
):

    def on_after_startup(self):
        self._logger.info("Refactor plugin!")

    def get_settings_defaults(self):
        return {
            "version_file": "/etc/refactor.version",
            "klipper_dir": "/home/debian/klipper"
        }

    def get_template_configs(self):
        return [
        ]

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
            get_versions=[]
        )

    def on_api_command(self, command, data):
        import flask
        if command == "get_versions":
            versions = {
                "refactor": {
                    "name": "Refactor",
                    "version": self.get_refactor_version()
                },
                "klipper": {
                    "name": "Klipper",
                    "version": self.get_klipper_version()
                }
            }
            self._logger.info(versions)
            return flask.jsonify(**versions)

    def on_api_get(self, request):
        return flask.jsonify(foo="bar")

    def get_refactor_version(self):
        with open("/etc/refactor.version", "r") as f:
            version = f.read().replace("\n", "")
            return version

    def get_klipper_version(self):
        import subprocess
        klipper_dir = self._settings.get(["klipper_dir"])
        path = "git -C "+klipper_dir+" describe --always --tags --long --dirty"
        try:
            return subprocess.check_output(path.split()).strip()
        except subprocess.CalledProcessError:
            return "Uknown"


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
