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
        self.versions = new ItemListHelper(
            "plugin_refactor_versions", {}, {},
            "name",
            [],
            [],
            5
        );

        self.availableRefactorVersions = ko.observable();
        self.selectedVersion = ko.observable();
        self.onBeforeBinding = function() {
            self.requestData();
        }
        self.installSelectedVersion = function() {
            self.runCommand("download_refactor", {
                "refactor_version": self.selectedVersion()
            }, function(status) {
                self.progressTimer = setInterval(self.checkProgress, 1000);
                self.isDownloading(true);
            });
        }
        self.cancelDownload = function() {
          self.runCommand("cancel_download", {}, function(status) {
              clearInterval(self.progressTimer);
              self.isDownloading(false);
          });
        }
        self.downloadProgress = ko.observable("0%");
        self.isDownloading = ko.observable(false);
        self.checkProgress = function() {
            self.runCommand("get_install_progress", {}, function(data) {
                self.downloadProgress((data.progress*100).toString()+"%");
                if(data.progress > 0.999){
                  clearInterval(self.progressTimer);
                  self.isDownloading(false);
                }
            });
        }
        self.changeBootMedia = function() {
            self.runCommand("change_boot_media", {}, function(data) {
                self.bootMedia(data.boot_media);
            });
        }

        self.requestData = function() {
            self.runCommand("get_data", {}, function(data) {
                var versions = [];
                _.each(_.keys(data.versions), function(key) {
                    versions.push({
                        key: key,
                        name: ko.observable(data.versions[key].name),
                        version: ko.observable(data.versions[key].version)
                    });
                });
                self.versions.updateItems(versions);
                self.bootMedia(data.boot_media);
                self.availableRefactorVersions(data.releases);
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
