var LotMap = {

    epsg4326: new OpenLayers.Projection("EPSG:4326"),
    epsg900913: new OpenLayers.Projection("EPSG:900913"),

    init: function(options, elem) {
        var t = this;
        this.options = $.extend({}, this.options, options);

        this.elem = elem;
        this.$elem = $(elem);

        this.olMap = new OpenLayers.Map(this.$elem.attr('id'), {
            controls: [
                new OpenLayers.Control.Navigation(),
                new OpenLayers.Control.Attribution(),
                new OpenLayers.Control.LoadingPanel(),
                new OpenLayers.Control.ZoomPanel(),
            ],
            restrictedExtent: this.createBBox(-75.066, 41.526, -72.746, 39.953), 
            zoomToMaxExtent: function() {
                this.setCenter(t.options.center, t.options.initialZoom);
            }
        });

        var cloudmade = new OpenLayers.Layer.CloudMade("CloudMade", {
            key: '781b27aa166a49e1a398cd9b38a81cdf',
            styleId: '15434',
            transitionEffect: 'resize'
        });
        this.olMap.addLayer(cloudmade);

        this.olMap.zoomToMaxExtent();

        return this;
    },

    options: {
        /*center: new OpenLayers.LonLat(-8230729.8555054, 4970948.0494563),*/
        center: new OpenLayers.LonLat(-8234102.434993, 4960767.039686),
        initialZoom: 11,
        addContentToPopup: function(popup, feature) { ; },
        type: null, 
        id: null, /* put something here if using type='single' */
        url: '/gardens/geojson?',
        queryString: '',
    },

    createBBox: function(lon1, lat1, lon2, lat2) {
        var b = new OpenLayers.Bounds();
        b.extend(this.getTransformedLonLat(lon1, lat1));
        b.extend(this.getTransformedLonLat(lon2, lat2));
        return b;
    },

    styles: {
        'default': {
            pointRadius: '5',
            fillColor: '#3f9438',
            fillOpacity: '0.4',
            strokeOpacity: '0.8',
            strokeWidth: 0,
        },
        'single': { 
            pointRadius: '6', 
            fillColor: '#f9ff51', 
            fillOpacity: '0.6',
        },
    },

    getStyles: function(style) {
        return new OpenLayers.StyleMap({'default': style, 'select': {pointRadius: 15}, 'temporary': {pointRadius: 10}});
    },

    getLayer: function(name, url, style) {
        var layer = new OpenLayers.Layer.Vector(name, {
            projection: this.olMap.displayProjection,
            strategies: [new OpenLayers.Strategy.Fixed()],
            styleMap: this.getStyles(style),
            protocol: new OpenLayers.Protocol.HTTP({
                url: url,
                format: new OpenLayers.Format.GeoJSON()
            })
        });
        this.olMap.addLayer(layer);
        return layer;
    },

    addControls: function(layers) {
        this.getControlHoverFeature(layers);
        this.selectControl = this.getControlSelectFeature(layers);
    },

    getControlSelectFeature: function(layers) {
        var selectControl = new OpenLayers.Control.SelectFeature(layers);
        var t = this;

        $.each(layers, function(i, layer) {
            layer.events.on({
                "featureselected": function(event) {
                    var feature = event.feature;
                    var popup = t.createAndOpenPopup(feature);
                    t.options.addContentToPopup(popup, feature);
                },
                "featureunselected": function(event) {
                    var feature = event.feature;
                    if(feature.popup) {
                        t.olMap.removePopup(feature.popup);
                        feature.popup.destroy();
                        delete feature.popup;
                    }
                },
            });
        });

        this.olMap.addControl(selectControl);
        selectControl.activate();   
        return selectControl;
    },

    createAndOpenPopup: function(feature) {
        var content = "<div style=\"min-width: 500px; min-height: 250px;\"></div>";
        var t = this;

        var popup = new OpenLayers.Popup.Anchored("chicken", 
                                    feature.geometry.getBounds().getCenterLonLat(),
                                    new OpenLayers.Size(500, 300),
                                    content,
                                    null, 
                                    true, 
                                    function(event) { t.selectControl.unselectAll(); });
        popup.panMapIfOutOfView = true;
        feature.popup = popup;
        this.olMap.addPopup(popup);

        // don't let the close box add whitespace to the popup
        var new_width = $('.olPopupContent').width() + $('.olPopupCloseBox').width();
        $('.olPopupContent').width(new_width);
        return $('#chicken_contentDiv');
    },

    getControlHoverFeature: function(layers) {
        var selectControl = new OpenLayers.Control.SelectFeature(layers, {
            hover: true,
            highlightOnly: true,
            renderIntent: 'temporary'
        });
        this.olMap.addControl(selectControl);
        selectControl.activate();   
        return selectControl;
    },

    hideLayer: function(name) {
        var layers = this.olMap.getLayersByName(name);
        if (layers.length == 0) return;
        layers[0].setVisibility(false);
    },

    showLayer: function(name) {
        var layers = this.olMap.getLayersByName(name);
        if (layers.length == 0) {
            this.loadLayer(name);
        }
        else {
            layers[0].setVisibility(true);
        }
    },

    layerUrls: {
        'City Councils': "resources/geojson/nycc.geojson",
        'City Council Labels': "resources/geojson/nycc_centroids.geojson",
        'Community Districts': "resources/geojson/nycd.geojson",
        'Community District Labels': "resources/geojson/nycd_centroids.geojson",
        'Boroughs': "resources/geojson/boroughs.geojson",
        'Borough Labels': "resources/geojson/borough_centroids.geojson",
    },

    loadLayer: function(name) {
        var layer = new OpenLayers.Layer.Vector(name, {
            projection: this.olMap.displayProjection,
            strategies: [new OpenLayers.Strategy.Fixed()],
            protocol: new OpenLayers.Protocol.HTTP({
                url: this.layerUrls[name],
                format: new OpenLayers.Format.GeoJSON(),
            }),
            styleMap: new OpenLayers.StyleMap({
                'default': {
                    'strokeWidth': 1,
                    'strokeColor': '#000',
                    'fillOpacity': 0,
                },
            }),
        });
        this.olMap.addLayer(layer);
    },

    hideLabelLayer: function(name) {
        var layers = this.olMap.getLayersByName(name);
        if (layers.length == 0) return;
        layers[0].setVisibility(false);
    },

    showLabelLayer: function(name) {
        var layers = this.olMap.getLayersByName(name);
        if (layers.length == 0) {
            this.loadLabelLayer(name);
        }
        else {
            layers[0].setVisibility(true);
        }
    },

    loadLabelLayer: function(name) {
        var layer = new OpenLayers.Layer.Vector(name, {
            projection: this.olMap.displayProjection,
            strategies: [new OpenLayers.Strategy.Fixed()],
            protocol: new OpenLayers.Protocol.HTTP({
                url: this.layerUrls[name],
                format: new OpenLayers.Format.GeoJSON(),
            }),
            styleMap: new OpenLayers.StyleMap({
                'default': {
                    'label': '${label}',
                },
            }),
        });
        this.olMap.addLayer(layer);
    },

    selectAndCenterOnGarden: function(fid) {
        var feature = this.surveyedGardensLayer.getFeatureByFid(fid);
        if (!feature) return;

        var l = new OpenLayers.LonLat(feature.geometry.x, feature.geometry.y);
        this.olMap.setCenter(l, 15);
        this.selectControl.unselectAll();
        this.selectControl.select(feature);
    },

    highlightGarden: function(fid) {
        var feature = this.olMap.layers[1].getFeatureByFid(fid);
        if (!feature) return;

        this.hoverControl.unselectAll();
        this.hoverControl.select(feature);
    },

    unhighlightGarden: function() {
        this.hoverControl.unselectAll();
    },

    getTransformedLonLat: function(longitude, latitude) {
        return new OpenLayers.LonLat(longitude, latitude).transform(this.epsg4326, this.epsg900913);
    },

};

$.plugin('lotmap', LotMap);
