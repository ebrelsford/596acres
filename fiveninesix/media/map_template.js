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

/*
 * Make UI match the given initial filters
 */
function set_initial_filters(f) {
    if (f['boroughs']) {
        $.each(f['boroughs'].split(','), function(i, borough) {
            $('.filters .boroughs :input[value="' + borough + '"]').attr('checked', 'yes');
        });
    }
    if (f['lot_types']) {
        $('.map-legend :input').removeAttr('checked');
        $.each(f['lot_types'].split(','), function(i, lot_type) {
            $('.map-legend :input[name="' + lot_type + '"]').attr('checked', 'yes');
        });
    }
    // min/max area are handled in slider
    // owner handled as select is initialized
}

/*
 * Get the currently selected boroughs.
 */
function get_selected_boroughs() {
    return $('.filters .boroughs :input:checked').map(function(i, element) {
        return $(element).val();
    }).get();
}

/*
 * Update the legend to show the correct counts for the selected boroughs.
 */
function update_counts() {
    $('.tally').addClass('loading');
    uri = URI('/lot/counts?').query($('#map').data('lotmap').exportFilters());
    $.getJSON(uri, function(data) {
        $.each(data, function(lot_type, count) {
            $('.map-legend .count.' + lot_type).text(count);
        });
        $('.tally').removeClass('loading');
    });
    $('.compare-text').text('');
}

function compare_size($el) {
    $el.addClass('selected');
    $('.tally').addClass('loading');
    var $count_row = $el.parent();
    $.getJSON('/size-compare/find/?acres=' + $count_row.find('.acres').text(),
        function(data) {
            $('.tally').removeClass('loading');
            if (!data.success) return;

            var text = '';
            if (data.factor === '1') {
                text = 'These lots are the same size as ' + data.name + '.';
            }
            else if (data.comparable_is === 'smaller') {
                text = 'These lots are ' + data.factor + ' times the size of ' + data.name + '.';
            }
            else if (data.comparable_is === 'bigger') {
                text = 'These lots are ' + data.fraction + ' the size of ' + data.name + '.';
            }
            $count_row.find('.compare-text')
                .text(text)
                .show();
        }
    );
}

$(document).ready(function() {
    // get filters, make UI match
    var filters = URI().query(true);
    set_initial_filters(filters);

    $('#map').lotmap({
        mobile: $('#map').hasClass('mobile'),
        filters: filters,
        fullScreen: true,
        zoomToFeatures: true,
        addContentToPopup: function(popup, feature) {
            // loading....
            var $loading_clone = $('.popup_loading').clone();
            $(popup).find('div').append($loading_clone.addClass('copy').show());

            if (feature.data.search_results) {
                var lonLat = feature.geometry.getBounds().getCenterLonLat();
                lonLat = $('#map').data('lotmap').getInverseLonLat(lonLat.lon, lonLat.lat);

                var params = {
                    latitude: lonLat.lat,
                    longitude: lonLat.lon,
                };
                var address = feature.data.address;
                if (address) params.address = address;
                var query = feature.data.query;
                if (query) params.query = query;
                $(popup).load('/oasis_popup/?' + $.param(params), function() {
                    // ....done loading
                    $loading_clone.remove();
                });
            }
            else {

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
            }

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
            if (f.data.search_results) return;

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

        onViewportChange: function() {
            update_counts();
        },
    });

    // update legend/tally to match given filters
    update_counts();

    $('#searchbar').search({
        map: $('#map').data('lotmap'),
        bounds: map_bounds,
    });

    $('#map_buttons').mapbuttons({
        $map: $('#map'),
    });

    var initial_min_area = filters['min_area'] || 0;
    var initial_max_area = filters['max_area'] || max_area_range;
    $('#area_slider').slider({
        range: true,
        max: max_area_range,
        min: 0,
        step: .01,
        values: [initial_min_area, initial_max_area],
        slide: function(event, ui) {
            update_area_display(ui.values[0], ui.values[1]);
        },
        change: function(event, ui) {
            $('#map').data('lotmap').filterByArea(ui.values[0], ui.values[1]);
            update_counts();
        },
    });
    update_area_display(initial_min_area, initial_max_area);

    $('.filters .agency select').attr('disabled', 'disabled');
    $.getJSON('/owners/json/', function(data) {
        $.each(data.owners, function(i, owner) {
            var option = $('<option></option>').text(owner[1]).attr('value', owner[0]);
            $('.filters .agency select').append(option);
        });
        $('.filters .agency select').removeAttr('disabled');
        
        // select initial owner
        $('.filters .agency option[value=' + filters['owner_id'] + ']').attr('selected', 'yes');
    });

    $('.filters .agency select').change(function() {
        var agency_id = $(this).find('option:selected').attr('value');
        $('#map').data('lotmap').filterByAgency(agency_id);
        update_counts();
    });

    $('.filters .boroughs :input').change(function() {
        var boroughs = get_selected_boroughs();

        // update map
        $('#map').data('lotmap').filterByBoroughs(boroughs);
        update_counts();
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

    $('.permalink a').click(function() {
        window.location.href = URI().query($('#map').data('lotmap').exportFilters());
        return false;
    });

    $('.download a').click(function() {
        window.location.href = '/lots/' + $(this).attr('class') + '?' + URI().query($('#map').data('lotmap').exportFilters()).query() + '&download=true';
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

    $('.compare-link').click(function(e) {
        compare_size($(this));
        e.preventDefault();
        return false;
    });

    $(document).mouseup(function (e) {
        // hide size comparison boxes
        var container = $('.compare-text');
        if (!container.is(e.target) && container.has(e.target).length === 0) {
            container.hide();
            $('.compare-link').removeClass('selected');
        }
    });
});
