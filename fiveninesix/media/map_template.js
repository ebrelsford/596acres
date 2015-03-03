/*
 * Update activity stream.
 */
function update_activity_stream() {
    var filters = null;
    if (activity_stream_visible_only()) {
        filters = $('#map').data('lotmap').exportFilters();
    }
    $('.activity-stream-container').data('activity_stream').load_activities(filters);
}

function activity_stream_visible_only() {
    return $('.activity-stream-filters input[name="show_visible_only"]:checked').length > 0;
}

$(document).ready(function() {
    $('.activity-stream-container').activity_stream();
    $('.activity-stream-filters input[name="show_visible_only"]').change(function() {
        update_activity_stream();
    });
});
