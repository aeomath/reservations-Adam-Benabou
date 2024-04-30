
var map;
var directionsService;
var directionsRenderer;

function calculateAndDisplayRoute(start, end) {
    var request = {
        origin: start,
        destination: end,
        travelMode: 'TRANSIT'
    };
    directionsService.route(request, function (result, status) {
        if (status == 'OK') {
            directionsRenderer.setDirections(result);
        }
    });
}

function initMap() {
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();

    var paris = new google.maps.LatLng(48.8566, 2.3522);
    var mapOptions = {
        zoom: 7,
        center: paris
    };
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    directionsRenderer.setMap(map);

    var startLat = 0;
    var startLng = 0;
    var endLat = 0;
    var endLng = 0;
    calculateAndDisplayRoute({ lat: startLat, lng: startLng }, { lat: endLat, lng: endLng });
}