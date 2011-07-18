

var Search = {

    init: function(options, elem) {
        var t = this;
        this.options = $.extend({}, this.options, options);

        this.elem = elem;
        this.$elem = $(elem);

        this.map = this.options.map;

        var t = this;

        if ('bounds' in this.options) {
            var bounds = this.options.bounds;
            this.latLngBounds = create_bounds(
                bounds.left,
                bounds.bottom,
                bounds.right,
                bounds.top
            );
        }

        this.$elem.keypress(function(e) {
            if (e.keyCode == '13') {
                e.preventDefault();
                t.searchByAddress();
            }
        });
        this.$elem.find('form').submit(function() {
            t.searchByAddress();
            return false;
        });
    },

    options: {
        map: null,
        bounds: {
            left: -180,
            bottom: -90,
            right: 180,
            top: 90,
        },
    },

    searchByAddress: function() {
        this.$elem.find('.warning').hide();
        this.$elem.find('.loading').show();

        var t= this;
        geocode(this.$elem.find("input[name='address']").val(), this.latLngBounds, function(results, status) {
            t.$elem.find('.loading').hide();
            var sublocality = get_component(results[0], 'sublocality');
            if (sublocality !== 'Brooklyn') {
                t.$elem.find('.warning').show();
                return;
            }

            var longitude = results[0].geometry.location.lng();
            var latitude = results[0].geometry.location.lat();
            var transformed = t.map.getTransformedLonLat(longitude, latitude);
            t.map.olMap.setCenter(transformed, 15);
            t.map.setSearchFeature(transformed);
        });
    },

};

$.plugin('search', Search);
