/* Copyright (c) 2011-2012 by OpenLayers Contributors (see authors.txt for
 * full list of contributors). Published under the Clear BSD license.
 * See http://svn.openlayers.org/trunk/openlayers/license.txt for the
 * full text of the license. */

/**
 * @requires OpenLayers/Control.js
 */

OpenLayers.Control.FullScreen = OpenLayers.Class(OpenLayers.Control, {

    type: OpenLayers.Control.TYPE_TOGGLE,

    fullscreenClass: 'fullscreen',

    setMap: function(map) {
        OpenLayers.Control.prototype.setMap.apply(this, arguments);

        // handle 'Esc' key press
        OpenLayers.Event.observe(document, "fullscreenchange", OpenLayers.Function.bind(function() {
            if (!document.fullscreenEnabled) {
                this.deactivate();
            }
        }, this));
    },

    activate: function() {
        if (OpenLayers.Control.prototype.activate.apply(this, arguments)) {
            if (this.map.div.requestFullscreen) {
                this.map.div.requestFullscreen();
            }
            OpenLayers.Element.addClass(this.map.div, this.fullscreenClass);
            this.map.updateSize();
            return true;
        } else {
            return false;
        }
    },

    deactivate: function() {
        if (OpenLayers.Control.prototype.deactivate.apply(this, arguments)) {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
            OpenLayers.Element.removeClass(this.map.div, this.fullscreenClass);
            this.map.updateSize();
            return true;
        } else {
            return false;
        }
    },

    CLASS_NAME: "OpenLayers.Control.FullScreen"
});
