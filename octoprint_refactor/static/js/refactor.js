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
          "plugin_refactor_versions",
          {},
          {},
          "name",
          [],
          [],
          5
      );

      self.onBeforeBinding = function() {
          self.requestData();
      }

      self.requestData = function() {
        self.run_command("get_data", function(data) {
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
        });
      }

      self.changeBootMedia = function() {
        self.run_command("change_boot_media", function(data) {
          self.bootMedia(data.boot_media);
        });
      }

      self.run_command = function(command, on_success) {
        $.ajax({
          url: API_BASEURL + "plugin/refactor",
          type:"POST",
          dataType: "json",
          contentType: "application/json; charset=UTF-8",
          data: JSON.stringify({ "command": command }),
          success: on_success
        });
      }
    }


    OCTOPRINT_VIEWMODELS.push({
        construct: RefactorViewModel,
        dependencies: [ "settingsViewModel" ],
        elements: ["#tab_plugin_refactor"]
    });
});
