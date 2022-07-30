/*
 * View model for OctoPrint-Refactor
 *
 * Author: Elias Bakken
 * License: AGPLv3
 */
$(function() {
    function RefactorViewModel(parameters) {
        var self = this;
        self.settings = parameters[0];
        self.bootMedia = ko.observable();
        self.rootfs = ko.observable();
        self.programVersions = ko.observable();
        self.remoteRefactorVersions = ko.observable();
        self.remoteSelectedVersion = ko.observable();
        self.localRefactorVersions = ko.observable();
        self.localSelectedVersion = ko.observable();
        self.downloadProgress = ko.observable("0%");
        self.isDownloading = ko.observable(false);
        self.isInstalling = ko.observable(false);
        self.installProgress = ko.observable("0%");
        self.isInstallFinished = ko.observable(false);
        self.isEmmcPresent = ko.observable(false);
        self.isUsbPresent = ko.observable(false);
        self.isSshEnabled = ko.observable(false);

        self.onBeforeBinding = function() {
            self.requestData();
        }
        self.changeBootMedia = function() {
            self.runCommand("change_boot_media", {}, function(data) {
                self.bootMedia(data.boot_media);
            });
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
                self.bootMedia(data.boot_media);
                self.isEmmcPresent(data.emmc_present);
                self.isUsbPresent(data.usb_present);
                self.rootfs(data.rootfs);
                self.isSshEnabled(data.ssh_enabled);
            });
        }
        self.runCommand = function(command, params, on_success) {
            $.ajax({
                url: API_BASEURL + "plugin/refactor",
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
        construct: RefactorViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#tab_plugin_refactor"]
    });
});
