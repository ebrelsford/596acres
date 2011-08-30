var LotMap = {

    //
    // projections
    //
    epsg4326: new OpenLayers.Projection("EPSG:4326"),
    epsg900913: new OpenLayers.Projection("EPSG:900913"),

    //
    // filters
    //
    minArea: null,
    maxArea: null,
    selectedAgency: null,
    lot_types: ['vacant',],

    //
    // styles
    //
    defaultStyle: new OpenLayers.StyleMap({
        'default': new OpenLayers.Style({             
            pointRadius: 3,
            fillColor: '#3f9438',
            fillOpacity: 0.8,
            strokeWidth: 0,
        }),
        'select': {
            pointRadius: 15,
        },
        'temporary': {
            pointRadius: 15,
        },
    }),

    gardenStyle: {
        strokeColor: 'black',
        strokeWidth: 1,
    },

    organizedStyle: {
        strokeColor: 'yellow',
        strokeWidth: 1,
    },

    borderStyle: {
        'strokeWidth': 3,
        'strokeColor': '#A4788C',
        'fillOpacity': 0,
    },

    init: function(options, elem) {
        var t = this;
        this.options = $.extend({}, this.options, options);

        this.elem = elem;
        this.$elem = $(elem);

        this.addRulesToStyle(this.defaultStyle.styles['default']);

        this.olMap = new OpenLayers.Map(this.$elem.attr('id'), {
            controls: [
                new OpenLayers.Control.Navigation(),
                new OpenLayers.Control.Attribution(),
                new OpenLayers.Control.LoadingPanel(),
                new OpenLayers.Control.ZoomPanel(),
            ],
            restrictedExtent: this.createBBox(-74.319, 40.948, -73.584, 40.476), 
            zoomToMaxExtent: function() {
                this.setCenter(t.options.center, t.options.initialZoom);
            },
            isValidZoomLevel: function(zoomLevel) {
                return (zoomLevel > 9 && zoomLevel < this.getNumZoomLevels());
            }
        });

        var cloudmade = new OpenLayers.Layer.CloudMade("CloudMade", {
            key: '781b27aa166a49e1a398cd9b38a81cdf',
            styleId: '15434',
            transitionEffect: 'resize',
        });
        this.olMap.addLayer(cloudmade);

        this.olMap.zoomToMaxExtent();

        this.lot_layer = this.getLayer('lots', this.options.url + this.getQueryString());
        this.lot_layer.events.on({
            'loadend': function() {
                if (t.lot_layer.features.length == 1) {
                    var feature = t.lot_layer.features[0];
                    t.centerOnFeature(t.lot_layer, feature.fid);
                    t.options.onLoad(feature);
                }
                else {
                    t.addControls([t.lot_layer]);
                }
            },
        });

        this.search_layer = new OpenLayers.Layer.Vector('search', {
            projection: this.olMap.displayProjection,
            styleMap: new OpenLayers.StyleMap({
                'default': {
                    pointRadius: '10',
                    fillColor: '#F3FA2D',
                    fillOpacity: '0.6',
                    strokeWidth: 1,
                    strokeColor: '#000000',
                },
            }),
        });
        this.olMap.addLayer(this.search_layer);

        return this;
    },

    options: {
        center: new OpenLayers.LonLat(-8234102.434993, 4960767.039686),
        initialZoom: 11,
        addContentToPopup: function(popup, feature) { ; },
        type: null, 
        url: '/lots/geojson?',
        queryString: '',
        onLoad: function(feature) {},
        onFeatureUnselect: function(feature) {},
        filter: true,
    },

    createBBox: function(lon1, lat1, lon2, lat2) {
        var b = new OpenLayers.Bounds();
        b.extend(this.getTransformedLonLat(lon1, lat1));
        b.extend(this.getTransformedLonLat(lon2, lat2));
        return b;
    },

    //
    // Add style rule to check for gardens and style them differently
    //
    addRulesToStyle: function(style) {
         style.addRules([
             new OpenLayers.Rule({
                 filter: new OpenLayers.Filter.Comparison({
                     type: OpenLayers.Filter.Comparison.EQUAL_TO,
                     property: 'is_garden',
                     value: true,
                 }),
                 symbolizer: this.gardenStyle,
             }),
             new OpenLayers.Rule({
                 filter: new OpenLayers.Filter.Comparison({
                     type: OpenLayers.Filter.Comparison.EQUAL_TO,
                     property: 'has_organizers',
                     value: true,
                 }),
                 symbolizer: this.organizedStyle,
             }),
             new OpenLayers.Rule({
                 elseFilter: true,
             }),
         ]);
     },

    getLayer: function(name, url) {
        var layer = new OpenLayers.Layer.Vector(name, {
            projection: this.olMap.displayProjection,
            strategies: [new OpenLayers.Strategy.Fixed()],
            styleMap: this.defaultStyle,
            protocol: new OpenLayers.Protocol.HTTP({
                url: url,
                format: new OpenLayers.Format.GeoJSON()
            })
        });
        this.olMap.addLayer(layer);
        return layer;
    },

    //
    // Add hover and select controls to the given layer
    //
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
                        t.options.onFeatureUnselect(feature);
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
        var content = "<div style=\"min-width: 250px; min-height: 250px;\"></div>";
        var t = this;

        var popup = new OpenLayers.Popup.Anchored("chicken", 
                                    feature.geometry.getBounds().getCenterLonLat(),
                                    new OpenLayers.Size(300, 300),
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
        'City Councils': "/media/geojson/nycc.geojson",
        'City Council Labels': "/media/geojson/nycc_centroids.geojson",
        'Community Districts': "/media/geojson/nycd.geojson",
        'Community District Labels': "/media/geojson/nycd_centroids.geojson",
        'Boroughs': "/media/geojson/boroughs.geojson",
        'Borough Labels': "/media/geojson/borough_centroids.geojson",
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
                'default': this.borderStyle,
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
                    'fontColor': '#7E2A70',
                    'fontSize': '18px',
                },
            }),
        });
        this.olMap.addLayer(layer);
    },

    centerOnFeature: function(layer, fid) {
        var feature = layer.getFeatureByFid(fid);
        if (!feature) return;

        var l = new OpenLayers.LonLat(feature.geometry.x, feature.geometry.y);
        this.olMap.setCenter(l, 15);
    },

    setSearchFeature: function(lonLat) {
        this.search_layer.removeAllFeatures();
        var feature = new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Point(lonLat.lon, lonLat.lat));
        this.search_layer.addFeatures([feature]);
    },

    getTransformedLonLat: function(longitude, latitude) {
        return new OpenLayers.LonLat(longitude, latitude).transform(this.epsg4326, this.epsg900913);
    },

    getInverseLonLat: function(longitude, latitude) {
        return new OpenLayers.LonLat(longitude, latitude).transform(this.epsg900913, this.epsg4326);
    },

    //
    // Get the query string for the currently chosen parameters
    //
    getQueryString: function() {
        if (!this.options.filter) return this.options.queryString;

        var extraParameters = "";
        if (this.selectedAgency !== null) {
            extraParameters += '&owner_id=' + this.selectedAgency;
        }
        if (this.minArea !== null) {
            extraParameters += '&min_area=' + this.minArea;
        }
        if (this.maxArea !== null) {
            extraParameters += '&max_area=' + this.maxArea;
        }
        if (this.lot_types) {
            extraParameters += '&lot_type=' + this.lot_types.join(',');
        }
        return this.options.queryString + extraParameters;
    },

    //
    // Reload the lot layer using filters that are set by the user, then updated
    // on this object using a filterBy*()
    //
    reloadLotLayer: function() {
        this.selectControl.unselectAll();
        this.olMap.removeLayer(this.lot_layer);
        this.lot_layer.destroy();

        this.lot_layer = this.getLayer('lots', this.options.url + this.getQueryString());

        this.addControls([this.lot_layer]);
        this.olMap.addLayer(this.lot_layer);
    },
    
    //
    // Filter by agency that owns the lots. Sets the selectedAgency and
    // ensures that the map is updated accordingly
    //
    filterByAgency: function(agency_id) {
        this.selectedAgency = agency_id === 'all' ? null : agency_id;
        this.reloadLotLayer();
    },

    //
    // Filter by area of the lots. Sets the min and max areas and
    // ensures that the map is updated accordingly
    //
    filterByArea: function(min, max) {
        this.minArea = min;
        this.maxArea = max;
        this.reloadLotLayer();
    },

    //
    // Filter by the type of lot. The currently allowed types are:
    //  * 'vacant' and
    //  * 'garden'
    // and they can independently be true or false.
    //
    filterByLotType: function(types) {
        this.lot_types = types;
        this.reloadLotLayer();
    },

};

$.plugin('lotmap', LotMap);
