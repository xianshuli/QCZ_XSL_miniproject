/**
 * Created by lixianshu on 10/11/15.
 */
$(document).ready(function () {

//var image1 = {
//    'url': "http://game.china.com/gbox/mh3g/act/000/015/948/8bb96cf9-918e-46e2-9599-3cad4e9a47f3.jpg",
//    'created': new Date("October 30, 2014 17:13:00"),
//    'lat': 0,
//    'lng': 90
//};
//var image2 = {
//    'url': "http://www.3dmgame.com/uploads/allimg/130709/180_130709182724_1.jpg",
//    'created': new Date(),
//    'lat': 0,
//    'lng': 92
//};
//var images = [image1, image2];

    var stream_key = "{{stream_key}}";
    console.log(stream_key);
    var indata = {"Stream_id": stream_key};

    $.ajax({
        url: '/geoViewRequest',
        data: indata,
        dataType: "json",
        type: "POST",
        success: function (data) {
            var southWest;
            var northEast;
            var marker_cluster1 = null;
            var marker_cluster2 = null;
            var images = [];
            for (var i = 0, len = data.length; i < len; ++i) {
                images.push({
                    "url": data[i].url,
                    "created": new Date(data[i].created),
                    "lat": data[i].lat,
                    "lng": data[i].lng
                });
                console.log(images[i]);
            }
            var southWest, northEast, lngSpan, latSpan;
            $('#map_canvas').gmap({'zoom': 2, 'disableDefaultUI': true}).bind('init', function (evt, map) {
                var bounds = map.getBounds();
                southWest = bounds.getSouthWest();
	            northEast = bounds.getNorthEast();
	            var lngSpan = northEast.lng() - southWest.lng();
	            var latSpan = northEast.lat() - southWest.lat();
                var lat = southWest.lat() + latSpan * Math.random();
		        var lng = southWest.lng() + lngSpan * Math.random();
                images.forEach(function (image) {
                    $('#map_canvas').gmap('addMarker', {
                        'position': new google.maps.LatLng(lat, lng)
                    }).mouseover(function () {
                        $('#map_canvas').gmap('openInfoWindow', {content: "<img src=" + image.url + " style='width:100px;height:100px;'>"}, this);
                    }).mouseout(function () {
                        $('#map_canvas').gmap('closeInfoWindow');
                    });
                });
                marker_cluster1 = new MarkerClusterer(map, $('#map_canvas').gmap('get', 'markers'));

                $('#map_canvas').gmap('set', 'MarkerClusterer', marker_cluster1);
                // To call methods in MarkerClusterer simply call
                // $('#map_canvas').gmap('get', 'MarkerClusterer').callingSomeMethod();
            });
            var showMin = (function () {
                var currMin = new Date();
                images.forEach(function (image) {
                    if (image.created && image.created < currMin) {
                        currMin = image.created;
                    }
                })
                return currMin;
            })();
            var showMax = new Date();
            console.log(typeof (showMax));
            //console.log('showmax ' + showMax);
            //console.log('showmin ' + showMin);
            //console.log('showmax ' + jQuery.type(showMax));
            //console.log('showmin ' + jQuery.type(showMin));
            //console.log('showmax time ' + showMax.getTime() / 86400000 / 365);
            //console.log('showmin time ' + showMin.getTime() / 86400000 / 365);
            //var minRange = Math.floor(showMax.getTime() / 86400000 - 366);
            $('#slider-range').slider({
                range: true,
                min: Math.floor(showMax.getTime() / 86400000 - 366),
                max: Math.floor(showMax.getTime() / 86400000),
                values: [showMin.getTime() / 86400000, showMax.getTime() / 86400000],
                slide: function (event, ui) {
                    var currentMin = new Date(ui.values[0] * 86400000);
                    var currentMax = new Date(ui.values[1] * 86400000 + 86400000);
                    $('#date-range').val(currentMin.toDateString() + ' - ' + currentMax.toDateString());
                    $('#map_canvas').gmap('clear', 'markers');
                    marker_cluster1.clearMarkers();
                    //if (marker_cluster2!=null) {
                    //    marker_cluster2.clearMarkers();
                    //}
                    console.log("currentMin " + currentMin);
                    console.log("currentMax " + currentMax);

                    images.forEach(function (image) {
                        console.log("image_created " + image.created);
                        if (image.created >= currentMin && image.created <= currentMax) {
                            var lat = southWest.lat() + latSpan * Math.random();
                            var lng = southWest.lng() + lngSpan * Math.random();
                            $('#map_canvas').gmap('addMarker', {
                                'position': new google.maps.LatLng(lat, lng)
                            }).mouseover(function () {
                                $('#map_canvas').gmap('openInfoWindow', {content: "<img src=" + image.url + " style='width:100px;height:100px;'>"}, this);
                            });
                        }
                    });
                    marker_cluster1 = new MarkerClusterer(map, $('#map_canvas').gmap('get', 'markers'));
                    $('#map_canvas').gmap('set', 'MarkerClusterer', marker_cluster1);
                }
            });
            $('#date-range').val(showMin.toDateString() + ' - ' + showMax.toDateString());
        }
    });
});