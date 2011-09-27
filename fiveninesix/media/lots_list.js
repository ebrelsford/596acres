
$(document).ready(function() {
    $('#map').lotmap({
        queryString: 'source=OASIS,Nominatim,Google&owner_type=city',   

        onFeatureHighlight: function(event) {
            $('#' + event.feature.fid).addClass('hovered');
        },

        onFeatureUnhighlight: function(event) {
            $('#' + event.feature.fid).removeClass('hovered');
        },

        filters: {
            lot_types: ['organizing',],
        },

        popups: false,
        select: false,
    });

    var map = $('#map').data('lotmap');

    $('.lot').hover(
        function(event) {
            map.highlightLot($(this).attr('id'));
        },
        function(event) {
            map.unhighlightLot();
        }
    );
});

