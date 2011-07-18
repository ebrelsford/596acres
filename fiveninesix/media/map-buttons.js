

var MapButtons = {

    init: function(options, elem) {
        var t = this;
        this.options = $.extend({}, this.options, options);

        this.elem = elem;
        this.$elem = $(elem);

        this.$map = this.options.$map;
        this.map = this.$map.data('lotmap');

        this.$elem.find('.dropdownable').hover(
            function() {
                $(this).addClass('expanded')
                    .find('.dropdown').show();
            },
            function() {
                $(this).removeClass('expanded')
                    .find('.dropdown').hide();
            }
        );

        this.$elem.find('#political_borders_selector input[type=radio]').change(function() {
            t.layerChanged($(this));
        });

        this.$elem.find('#political_borders_selector #labels input').change(function() {
            t.labelsChanged($(this).is(':checked'));
        });
    },

    options: {
        // the map that gardens are displayed on
        $map: null,
    },

    idsToLayerNames: {
        'boroughs': 'Boroughs',
        'city_councils': 'City Councils',
        'community_districts': 'Community Districts',
    },
    idsToLabelLayerNames: {
        'boroughs': 'Borough Labels',
        'city_councils': 'City Council Labels',
        'community_districts': 'Community District Labels',
    },

    layerChanged: function(radio) {
        var id = radio.parent().attr('id');
        if (radio.is(':checked')) {
            this.layerSelected(id);
        }
        else {
            this.layerDeselected(id);
        }

    },

    layerSelected: function(id) {
        this.$elem.find('#political_borders_selector input[type=radio]:not(:checked)').change();
        if (id !== 'none') {
            this.map.showLayer(this.idsToLayerNames[id]);
            if (this.$elem.find('#political_borders_selector #labels input').is(':checked')) {
                this.map.showLabelLayer(this.idsToLabelLayerNames[id]);
            }
        }
    },

    layerDeselected: function(id) {
        if (id !== 'none') {
            this.map.hideLayer(this.idsToLayerNames[id]);
            if (this.$elem.find('#political_borders_selector #labels input').is(':checked')) {
                this.map.hideLabelLayer(this.idsToLabelLayerNames[id]);
            }
        }
    },

    labelsChanged: function(show) {
        var selected_borders_id = this.$elem.find('#political_borders_selector input[type=radio]:checked').parent().attr('id');
        if (show) {
            if (selected_borders_id !== 'none') this.map.showLabelLayer(this.idsToLabelLayerNames[selected_borders_id]);
        }
        else {
            if (selected_borders_id !== 'none') this.map.hideLabelLayer(this.idsToLabelLayerNames[selected_borders_id]);
        }
    },

};

$.plugin('mapbuttons', MapButtons);
