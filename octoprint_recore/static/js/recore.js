/*
 * View model for OctoPrint-Recore
 *
 * Author: Elias Bakken
 * License: AGPLv3
 */
$(function() {
    function RecoreViewModel(parameters) {
        var self = this;
        self.settings = parameters[0];
        self.programVersions = ko.observable();
        self.isSshEnabled = ko.observable(false);

        self.onBeforeBinding = function() {
            self.requestData();
        }
        self.disableSsh = function() {
            self.runCommand("set_ssh_enabled", {"is_enabled": false}, function(data) {
                self.isSshEnabled(data.ssh_enabled);
            });
        }
        self.enableSsh = function() {
            self.runCommand("set_ssh_enabled", {"is_enabled": true}, function(data) {
                self.isSshEnabled(data.ssh_enabled);
            });
        }
        self.requestData = function() {
            self.runCommand("get_data", {}, function(data) {
                self.programVersions(data.versions);
                self.isSshEnabled(data.ssh_enabled);
            });
        }
        self.runCommand = function(command, params, on_success) {
            $.ajax({
                url: API_BASEURL + "plugin/recore",
                type: "POST",
                dataType: "json",
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify({
                    "command": command,
                    ...params
                }),
                success: on_success
            });
        }
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: RecoreViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#tab_plugin_recore"]
    });
});
