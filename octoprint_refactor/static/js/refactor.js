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
          $.ajax({
            url: API_BASEURL + "plugin/refactor",
            type:"POST",
            dataType: "json",
            contentType: "application/json; charset=UTF-8",
            data: JSON.stringify({
                "command": "get_versions"
            }),
            success: function(data) {
                var versions = [];
                _.each(_.keys(data), function(key) {
                    versions.push({
                        key: key,
                        name: ko.observable(data[key].name),
                        version: ko.observable(data[key].version)
                    });
                });
                self.versions.updateItems(versions);
            }
          });
        };
    }


    OCTOPRINT_VIEWMODELS.push({
        construct: RefactorViewModel,
        dependencies: [ "settingsViewModel" ],
        elements: ["#tab_plugin_refactor"]
    });
});
