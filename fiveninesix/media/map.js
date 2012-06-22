var LotMap = {

    //
    // projections
    //
    epsg4326: new OpenLayers.Projection("EPSG:4326"),
    epsg900913: new OpenLayers.Projection("EPSG:900913"),

    //
    // filters
    //
    boroughs: ['Brooklyn', 'Manhattan', 'Queens',],
    min_area: null,
    max_area: null,
    selectedAgency: null,
    lot_types: ['vacant','organizing','accessed','private_accessed'],

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

    mobileStyle: new OpenLayers.StyleMap({
        'default': new OpenLayers.Style({             
            pointRadius: 10,
            fillColor: '#3f9438',
            fillOpacity: 0.8,
            strokeWidth: 0,
        }),
        'select': {
            pointRadius: 20,
        },
        'temporary': {
            pointRadius: 20,
        },
    }),

    gardenStyle: {
        strokeColor: 'black',
        strokeWidth: 2,
    },

    organizedStyle: {
        strokeColor: '#DFCB00',
        strokeWidth: 2,
    },

    groupHasAccessStyle: {
        fillColor: '#FF0DFF',
        strokeColor: '#DFCB00',
        strokeWidth: 2,
        pointRadius: 7,
    },

    privateStyle: {
        fillColor: '#509EF2',
        strokeWidth: 0,
    },

    privateAccessedStyle: {
        fillColor: '#3C8FE8',
        pointRadius: 7,
        strokeColor: '#FF0DFF',
        strokeWidth: 2,
    },

    gutterspaceStyle: {
        pointRadius: 2,
        fillColor: '#F00',
    },

    recentChangesStyle: {
        pointRadius: 10,
    },

    detailStyle: {
        pointRadius: 15,
        fillOpacity: 1,
    },
    detailUnhighlightedStyle: {
        fillOpacity: .3,
        strokeOpacity: .3,
    },

    borderStyle: {
        strokeWidth: 3,
        strokeColor: '#A4788C',
        fillOpacity: 0,
    },
    
    searchStyle: {
        pointRadius: 10,
        fillColor: '#F3FA2D',
        fillOpacity: 0.6,
        strokeWidth: 1,
        strokeColor: '#000000',
    },

    init: function(options, elem) {
        var t = this;
        this.options = $.extend({}, this.options, options);

        if (this.options['filters']) {
            this.readFilters(this.options['filters']);
        }

        this.elem = elem;
        this.$elem = $(elem);

        this.style = this.defaultStyle;
        if (this.options.mobile) {
            this.style = this.mobileStyle;
        }
        this.addRulesToStyle(this.style.styles['default']);

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

        if (this.options.fullScreen) {
            var panel = new OpenLayers.Control.Panel();
            panel.addControls([new OpenLayers.Control.FullScreen()]);
            this.olMap.addControl(panel);
        }

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
                t.options.onLoad();
                if (t.options.detailView) {
                    t.centerOnFeature(t.lot_layer, t.options.detailFid);
                }
                else {
                    if (t.options.zoomToFeatures) {
                        var features_extent = t.lot_layer.getDataExtent(); 
                        t.olMap.zoomToExtent(features_extent, false);
                    }
                    t.addControls([t.lot_layer]);
                }
            },
        });

        this.search_layer = new OpenLayers.Layer.Vector('search', {
            projection: this.olMap.displayProjection,
            styleMap: new OpenLayers.StyleMap({
                'default': this.searchStyle,
            }),
        });
        this.olMap.addLayer(this.search_layer);

        return this;
    },

    options: {
        /*
         * map options
         */

        // the center of the map, in web mercator
        center: new OpenLayers.LonLat(-8232243.3222529, 4970015.5128625),

        // map will focus on one BBL, eg for the lot's page
        detailView: false,

        // map can go into fullscreen
        fullScreen: false,

        // the zoom for the map
        initialZoom: 10,

        // map will be displayed on a mobile device
        mobile: false,

        // allow popups
        popups: true,

        // allow lot selection
        select: true,

        // zoom to the lot features on load
        zoomToFeatures: false,

        /*
         * lot data options
         */

        // initial filters when querying for lot data
        filters: {},

        // the base query when requesting lot data
        queryString: '',

        // the base url data for the lot layer will come from
        url: '/lots/geojson?',

        /*
         * callbacks
         */
        addContentToPopup: function(popup, feature) {},
        onFeatureSelect: function(feature) {},
        onFeatureUnselect: function(feature) {},
        onFeatureHighlight: function(feature) {},
        onFeatureUnhighlight: function(feature) {},
        onLoad: function() {},
    },

    readFilters: function(f) {
        if (f['boroughs']) {
            this.boroughs = f['boroughs'].split(',');
        }
        if (f['lot_types']) {
            this.lot_types = f['lot_types'].split(',');
        }
        if (f['max_area']) {
            this.max_area = f['max_area'];
        }
        if (f['min_area']) {
            this.min_area = f['min_area'];
        }
        if (f['owner_id']) {
            this.selectedAgency = f['owner_id'];
        }
        if (f['lat'] && f['lon']) {
            this.options.center = this.getTransformedLonLat(f['lon'], f['lat']);
            this.options.zoomToFeatures = false;
        }
        if (f['z']) {
            this.options.initialZoom = f['z'];
            this.options.zoomToFeatures = false;
        }
    },

    exportFilters: function() {
        var center = this.olMap.getCenter();
        center = this.getInverseLonLat(center.lon, center.lat);

        filters = {
            'boroughs': this.boroughs.join(','),
            'lot_types': this.lot_types.join(','),
            'lat': Math.round(center.lat * 10000) / 10000.0,
            'lon': Math.round(center.lon * 10000) / 10000.0,
            'z': this.olMap.getZoom(),
        };
        if (this.max_area) filters['max_area'] = this.max_area;
        if (this.min_area) filters['min_area'] = this.min_area;
        if (this.selectedAgency) filters['owner_id'] = this.selectedAgency;
        return filters;
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
        var rules = [];

        rules.push(new OpenLayers.Rule({
            filter: new OpenLayers.Filter.Comparison({
                type: OpenLayers.Filter.Comparison.EQUAL_TO,
                property: 'is_garden',
                value: true,
            }),
            symbolizer: this.gardenStyle,
        }));

        rules.push(new OpenLayers.Rule({
            filter: new OpenLayers.Filter.Comparison({
                type: OpenLayers.Filter.Comparison.EQUAL_TO,
                property: 'has_organizers',
                value: true,
            }),
            symbolizer: this.organizedStyle,
        }));

        rules.push(new OpenLayers.Rule({
            filter: new OpenLayers.Filter.Comparison({
                type: OpenLayers.Filter.Comparison.EQUAL_TO,
                property: 'group_has_access',
                value: true,
            }),
            symbolizer: this.groupHasAccessStyle,
        }));

        rules.push(new OpenLayers.Rule({
            filter: new OpenLayers.Filter.Logical({
                type: OpenLayers.Filter.Logical.OR,
                filters: [
                    new OpenLayers.Filter.Comparison({
                        type: OpenLayers.Filter.Comparison.EQUAL_TO,
                        property: 'accessible',
                        value: false,
                    }),
                    new OpenLayers.Filter.Comparison({
                        type: OpenLayers.Filter.Comparison.EQUAL_TO,
                        property: 'actual_use',
                        value: 'gutterspace',
                    }),
                ],
            }),
            symbolizer: this.gutterspaceStyle,
        }));

        rules.push(new OpenLayers.Rule({
            filter: new OpenLayers.Filter.Comparison({
                type: OpenLayers.Filter.Comparison.EQUAL_TO,
                property: 'owner_type',
                value: 'private',
            }),
            symbolizer: this.privateStyle,
        }));

        rules.push(new OpenLayers.Rule({
            filter: new OpenLayers.Filter.Logical({
                type: OpenLayers.Filter.Logical.AND,
                filters: [
                    new OpenLayers.Filter.Comparison({
                        type: OpenLayers.Filter.Comparison.EQUAL_TO,
                        property: 'owner_type',
                        value: 'private',
                    }),
                    new OpenLayers.Filter.Comparison({
                        type: OpenLayers.Filter.Comparison.EQUAL_TO,
                        property: 'group_has_access',
                        value: true,
                    }),
                ],
            }),
            symbolizer: this.privateAccessedStyle,
        }));

        rules.push(new OpenLayers.Rule({
            filter: new OpenLayers.Filter.Comparison({
                type: OpenLayers.Filter.Comparison.NOT_EQUAL_TO,
                property: 'recent_change',
                value: null,
            }),
            symbolizer: this.recentChangesStyle,
        }));

        if (this.options.detailView) {
            rules.push(new OpenLayers.Rule({
                filter: new OpenLayers.Filter.Logical({
                    type: OpenLayers.Filter.Logical.NOT,
                    filters: [
                        new OpenLayers.Filter.FeatureId({
                            fids: [this.options.detailFid],
                        }),
                    ],
                }),
                symbolizer: this.detailUnhighlightedStyle,
            }));
            rules.push(new OpenLayers.Rule({
                filter: new OpenLayers.Filter.FeatureId({
                    fids: [this.options.detailFid],
                }),
                symbolizer: this.detailStyle,
            }));
        }

        if (this.options.mobile) {
            rules.push(new OpenLayers.Rule({
                minScaleDenominator: 100000,
                symbolizer: {
                    pointRadius: 3,
                },
            }));
        }

        rules.push(new OpenLayers.Rule({
            elseFilter: true,
        }));

         style.addRules(rules);
     },

    getLayer: function(name, url) {
        var layer = new OpenLayers.Layer.Vector(name, {
            projection: this.olMap.displayProjection,
            strategies: [
                new OpenLayers.Strategy.Fixed(),
            ],
            styleMap: this.style,
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
        var t = this;
        this.hoverControl = this.getControlHoverFeature(layers);
        if (t.options.select) {
            this.selectControl = this.getControlSelectFeature(layers);
        }
    },

    removeControls: function() {
        var t = this;
        this.hoverControl.deactivate();
        this.olMap.removeControl(this.hoverControl);
        if (t.options.select) {
            this.selectControl.deactivate();
            this.olMap.removeControl(this.selectControl);
        }
    },

    getControlSelectFeature: function(layers) {
        var selectControl = new OpenLayers.Control.SelectFeature(layers);
        var t = this;

        $.each(layers, function(i, layer) {
            layer.events.on({
                "featureselected": function(event) {
                    if (t.options.popups) {
                        var feature = event.feature;
                        var popup = t.createAndOpenPopup(feature);
                        t.options.addContentToPopup(popup, feature);
                    }
                    t.options.onFeatureSelect(feature);
                },
                "featureunselected": function(event) {
                    var feature = event.feature;
                    if(t.options.popups && feature.popup) {
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
        var t = this;

        var popup_width = 300;
        var map_width = t.$elem.innerWidth();
        var max_width = map_width - 65;
        if (popup_width > max_width) popup_width = max_width;
        var content_div_width = popup_width - 50;

        var popup_height = 300;
        var map_height = t.$elem.innerHeight();
        var max_height = map_height - 65;
        if (popup_height > max_height) popup_height = max_height;
        var content_div_height = popup_height - 50;

        var content = "<div style=\"width: " + content_div_width + "px !important; min-height: " + content_div_height + "px;\"></div>";
        var popup = new OpenLayers.Popup.Anchored("chicken", 
                                    feature.geometry.getBounds().getCenterLonLat(),
                                    new OpenLayers.Size(popup_width, popup_height),
                                    content,
                                    null, 
                                    true, 
                                    function(event) { t.selectControl.unselectAll(); });
        popup.panMapIfOutOfView = true;
        feature.popup = popup;
        this.olMap.addPopup(popup);

        // don't let the close box add whitespace to the popup
        $('.olPopupContent').width($('.olPopupContent').width() + 20);
        return $('#chicken_contentDiv');
    },

    getControlHoverFeature: function(layers) {
        var selectControl = new OpenLayers.Control.SelectFeature(layers, {
            hover: true,
            highlightOnly: true,
            renderIntent: 'temporary',
        });
        selectControl.events.on({
            'featurehighlighted': this.options.onFeatureHighlight,
            'featureunhighlighted': this.options.onFeatureUnhighlight,
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
        var extraParameters = "";
        if (this.boroughs) {
            extraParameters += '&boroughs=' + this.boroughs.join(',');
        }
        if (this.selectedAgency !== null) {
            extraParameters += '&owner_id=' + this.selectedAgency;
        }
        if (this.min_area !== null) {
            extraParameters += '&min_area=' + this.min_area;
        }
        if (this.max_area !== null) {
            extraParameters += '&max_area=' + this.max_area;
        }
        if (this.lot_types) {
            extraParameters += '&lot_types=' + this.lot_types.join(',');
        }
        return this.options.queryString + extraParameters;
    },

    //
    // Reload the lot layer using filters that are set by the user, then updated
    // on this object using a filterBy*()
    //
    reloadLotLayer: function(center_on_load) {
        if (this.options.select) {
            this.selectControl.unselectAll();
        }
        this.removeControls();
        this.olMap.removeLayer(this.lot_layer);
        this.lot_layer.destroy();

        this.lot_layer = this.getLayer('lots', this.options.url + this.getQueryString());
        var t = this;
        this.lot_layer.events.on({
            'loadend': function() {
                t.options.onLoad();
                if (center_on_load) {
                    var features_extent = t.lot_layer.getDataExtent(); 
                    t.olMap.zoomToExtent(features_extent, false);
                }
                t.addControls([t.lot_layer]);
            },
        });

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
        this.min_area = min;
        this.max_area = max;
        this.reloadLotLayer();
    },

    //
    // Filter by boroughs.
    //
    filterByBoroughs: function(boroughs) {
        this.boroughs = boroughs;
        this.reloadLotLayer(true);
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

    highlightLot: function(fid) {
        var feature = this.olMap.layers[1].getFeatureByFid(fid);
        if (!feature) return;  

        this.hoverControl.unselectAll();
        this.hoverControl.select(feature);
    },

    unhighlightLot: function() { 
        this.hoverControl.unselectAll();
    },

};

$.plugin('lotmap', LotMap);
