var max_area_range = 3;
var sv = new google.maps.StreetViewService();

var map_bounds = {
    left: -74.569, 
    top: 41.069, 
    right: -73.366, 
    bottom: 40.303,
};

function show_with_streetview(id, feature) {
    if (feature == null) return;
    var lon = feature.geometry.x;
    var lat = feature.geometry.y;
    var point = $('#map').data('lotmap').getInverseLonLat(lon, lat);

    sv.getPanoramaByLocation(new google.maps.LatLng(point.lat, point.lon), 50, function(result, status) {
        if (status == google.maps.StreetViewStatus.OK) {
            $('#' + id).show();
            new google.maps.StreetViewPanorama(document.getElementById(id), {
                addressControl: false,
                pano: result.location.pano,
            });
        }
        else {
            $('#streetview-error').slideDown();
        }
    });
}

function update_area_display(min, max) {
    if (max === max_area_range) {
        max += '+';
    }
    $('#area .min').text(min);
    $('#area .max').text(max);
}

function is_in(longitude, latitude, bounds) {
    return latitude <= bounds.top &&
        latitude >= bounds.bottom &&
        longitude <= bounds.right &&
        longitude >= bounds.left;
}

$(document).ready(function() {
    $('#map').lotmap({
        mobile: $('#map').hasClass('mobile'),
        queryString: 'boroughs=Brooklyn&owner_type=city,private',   
        addContentToPopup: function(popup, feature) {
            // loading....
            var $loading_clone = $('.popup_loading').clone();
            $(popup).find('div').append($loading_clone.addClass('copy').show());

            $(popup).load('/lot/' + feature.fid + '/tabs/', function() {
                // ....done loading
                $loading_clone.remove();

                // link to owner tab
                $(popup).find('.tabs').tabs()
                    .find('tr.owner').click(function() {
                        $(this).parents('.tabs').tabs('select', '#owner');
                        return false;
                    });

                // link to organize
                $(popup).find('.organize-link').click(function() {
                    $(popup).find('.tabs').tabs('select', '#organize');
                    return false;
                });
            });

            // street view
            show_with_streetview('streetview', feature);
        },

        onFeatureSelect: function(event) {
            $('.highlight_box').hide();
        },

        onFeatureUnselect: function(feature) {
            $('.streetview').slideUp();
        },

        onFeatureHighlight: function(event) {
            var f = event.feature;
            var acres = f.data.area;
            if (acres === 0) {
                acres = 'almost 0';
            }
            $('.highlight_box').text(acres + ' acres').show();

            var recent_change = f.data.recent_change;
            if (recent_change) {
                $('.highlight_box').append('<div class="recent_change">' + recent_change + '</div>');
            }
            
            var feature_position = $('#map').data('lotmap').olMap.getPixelFromLonLat(new OpenLayers.LonLat(f.geometry.x, f.geometry.y));

            var map_offset = $('#map').offset();

            $('.highlight_box').offset({
                left: feature_position.x + map_offset.left + 10,
                top: feature_position.y + map_offset.top - 10,
            });
        },

        onFeatureUnhighlight: function(event) {
            $('.highlight_box').hide();
        },
    });

    $('#searchbar').search({
        map: $('#map').data('lotmap'),
        bounds: map_bounds,
    });

    $('#map_buttons').mapbuttons({
        $map: $('#map'),
    });

    $('#area_slider').slider({
        range: true,
        max: max_area_range,
        min: 0,
        step: .01,
        values: [0, max_area_range],
        slide: function(event, ui) {
            update_area_display(ui.values[0], ui.values[1]);
        },
        change: function(event, ui) {
            $('#map').data('lotmap').filterByArea(ui.values[0], ui.values[1]);
        },
    });
    update_area_display(0, max_area_range);

    $('.filters .agency select').attr('disabled', 'disabled');
    $.getJSON('/owners/json/', function(data) {
        $.each(data.owners, function(i, owner) {
            var option = $('<option></option>').text(owner[1]).attr('value', owner[0]);
            $('.filters .agency select').append(option);
        });
        $('.filters .agency select').removeAttr('disabled');
    });

    $('.filters .agency select').change(function() {
        var agency_id = $(this).find('option:selected').attr('value');
        $('#map').data('lotmap').filterByAgency(agency_id);
    });

    $('#searchbar input[name="current_location"]').click(function() {
        navigator.geolocation.getCurrentPosition(
            function(loc) {
                var lon = loc.coords.longitude,
                    lat = loc.coords.latitude;
                var map = $('#map').data('lotmap');

                if (is_in(lon, lat, map_bounds)) {
                    var transformed = map.getTransformedLonLat(lon, lat);
                    map.olMap.setCenter(transformed, 15);
                    map.setSearchFeature(transformed);
                }
                else {
                    $('#searchbar .warning').text("Sorry, the location we found for you is outside of New York. Try searching?").show();
                }
            },
            function(err) {
                if (err.code !== 1) {
                    $('#searchbar .warning').text("Sorry, we're having a hard time finding your location. Try searching?").show();
                }
            }
        );
    });

    $('.download a').click(function() {
        window.location.href = '/lots/' + $(this).attr('class') + '?' + $('#map').data('lotmap').getQueryString() + '&download=true';
        return false;
    });

    var help = $('#map_overlay').help({
        parent_div: $('#map'),
    }).data('help');

    $('#map_overlay .close').click(function() {
        if (help !== undefined) {
            help.hide_help();
        }
        $.getJSON('/sessions/hide_map_overlay/');
        return false;
    });

    $(window).load(function() {
        if (help !== undefined) {
            help.show_help();
        }
    });

});
