var max_area_range = 100000;

var brooklyn_bounds = {
    left: -74.319, 
    top: 40.948, 
    right: -73.584, 
    bottom: 40.476,
};

function show_with_streetview(id, feature) {
    var lon = feature.geometry.x;
    var lat = feature.geometry.y;
    var point = $('#map').data('lotmap').getInverseLonLat(lon, lat);

    $('#' + id).slideDown();
    var pan = new google.maps.StreetViewPanorama(document.getElementById(id), {
        position: new google.maps.LatLng(point.lat, point.lon),
    });
}

function load_organize_form($tab, url) {
    $tab.load(url, on_organize_form_submit($tab, url));
}

function submit_organize_form($tab, url) {
    $tab.load(url, $tab.find('form').serializeArray(), on_organize_form_submit($tab, url));
}

function on_organize_form_submit($tab, url) {
    return function() {
        $tab.find('form').submit(function(e) {
            submit_organize_form($tab, url);
            return false;
        });  
    }
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
        queryString: 'source=OASIS,Nominatim,Google&owner_type=city',   
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

                // form-in-a-tab
                $organize_tab = $(popup).find('.tabs #organize');
                $organize_tab.find('a.add_organizer').click(function() {
                    load_organize_form($organize_tab, '/lot/' + feature.fid + '/organizers/add/ajax/');
                    return false;
                });
            });

            // street view
            show_with_streetview('streetview', feature);
        },

        onFeatureUnselect: function(feature) {
            $('#streetview').slideUp();
        }
    });

    $('#searchbar').search({
        map: $('#map').data('lotmap'),
        bounds: brooklyn_bounds,
    });

    $('#map_buttons').mapbuttons({
        $map: $('#map'),
    });

    $('#area_slider').slider({
        range: true,
        min: 1,
        max: max_area_range,
        values: [1, max_area_range],
        slide: function(event, ui) {
            update_area_display(ui.values[0], ui.values[1]);
        },
        change: function(event, ui) {
            $('#map').data('lotmap').restrictByArea(ui.values[0], ui.values[1]);
        },
    });
    update_area_display(1, max_area_range);

    $('#searchbar input[name="current_location"]').click(function() {
        navigator.geolocation.getCurrentPosition(
            function(loc) {
                var lon = loc.coords.longitude,
                    lat = loc.coords.latitude;
                var map = $('#map').data('lotmap');

                if (is_in(lon, lat, brooklyn_bounds)) {
                    var transformed = map.getTransformedLonLat(lon, lat);
                    map.olMap.setCenter(transformed, 15);
                    map.setSearchFeature(transformed);
                }
                else {
                    $('#searchbar .warning').text("Sorry, the location we found for you is outside of Brooklyn. Try searching?").show();
                }
            },
            function(err) {
                if (err.code !== 1) {
                    $('#searchbar .warning').text("Sorry, we're having a hard time finding your location. Try searching?").show();
                }
            }
        );
    });
});
