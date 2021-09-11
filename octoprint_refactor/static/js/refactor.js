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

        self.onBeforeBinding = function() {
            self.requestData();
        }
        self.downloadSelectedVersion = function() {
            self.runCommand("download_refactor", {
                "refactor_version": self.remoteSelectedVersion()
            }, function(status) {
                self.downloadProgressTimer = setInterval(self.checkDownloadProgress, 1000);
                self.isDownloading(true);
            });
        }
        self.cancelDownload = function() {
          self.runCommand("cancel_download", {}, function(status) {
              clearInterval(self.downloadProgressTimer);
              self.isDownloading(false);
          });
        }
        self.checkDownloadProgress = function() {
            self.runCommand("get_download_progress", {}, function(data) {
                self.downloadProgress((data.progress*100).toFixed(1).toString()+"%");
                if(data.is_finished){
                  clearInterval(self.downloadProgressTimer);
                  self.isDownloading(false);
                  self.requestData();
                }
            });
        }
        self.checkInstallProgress = function() {
            self.runCommand("get_install_progress", {}, function(data) {
                self.installProgress((data.progress*100).toString()+"%");
                if(data.is_finished){
                  clearInterval(self.installProgressTimer);
                  self.isInstalling(false);
                  self.isInstallFinished(true);
                  self.requestData();
                }
            });
        }
        self.installSelectedVersion = function() {
            self.runCommand("install_refactor", {
                "filename": self.localSelectedVersion()
            }, function(status) {
                self.installProgressTimer = setInterval(self.checkInstallProgress, 1000);
                self.isInstalling(true);
                self.isInstallFinished(false);
            });
        }
        self.changeBootMedia = function() {
            self.runCommand("change_boot_media", {}, function(data) {
                self.bootMedia(data.boot_media);
            });
        }
        self.requestData = function() {
            self.runCommand("get_data", {}, function(data) {
                self.programVersions(data.versions);
                self.bootMedia(data.boot_media);
                self.remoteRefactorVersions(data.releases);
                self.localRefactorVersions(data.locals);
                self.isEmmcPresent(data.emmc_present);
                self.isUsbPresent(data.usb_present);
                self.rootfs(data.rootfs);
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
