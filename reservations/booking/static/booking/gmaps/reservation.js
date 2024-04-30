/**
 * Fichier JS pour la gestion de l'API Google Maps sur l'onglet reservation
 * 
 * De nombreux éléments de ce fichier sont inspirés de la documentation officielle de l'api de google maps
 * 
 * https://developers.google.com/maps/documentation/javascript/
 * 
 */

// Déclaration de variables globales pour la carte, le service de directions et le rendu des directions.
var map;
var directionsService;
var directionsRenderer;


// fonction qui se lance lorsque qu'on charge l'api google map
async function initMap() {
    // On importe les librairies nécessaires (utilisation de l'api dynamique ! )
    const { Map } = await google.maps.importLibrary("maps");
    const { DirectionsRenderer } = await google.maps.importLibrary("routes");
    const { DirectionsService } = await google.maps.importLibrary("routes");

    directionsService = new DirectionsService()
    directionsRenderer = new DirectionsRenderer({ suppressMarkers: true, suppressInfoWindows: false })

    // On crée une carte centrée sur Paris
    var paris = new google.maps.LatLng(48.8566, 2.3522);
    var mapOptions = {
        zoom: 7,
        center: paris,
        region: 'fr',
        language: 'fr',
        mapTypeId: 'roadmap'
    };
    map = new Map(document.getElementById('map'), mapOptions);
    directionsRenderer.setMap(map);
    directionsRenderer.setPanel(document.getElementById('directionsPanel'));
}

/**
 * 
 *  Fonction pour calculer et afficher l'itinéraire entre deux points
 * @param  start Position de départ (latitude,longitude)
 * @param end Position d'arrivée (latitude,longitude)
 */
async function calculateAndDisplayRoute(start, end, departureTime) {
    // on attend que l'api google map soit chargée
    await initMap()

    departureTime.setMinutes(departureTime.getMinutes() - 10)// Pour éviter de rater le train :)
    // Création d'une requête pour le service de directions.
    var request = {
        origin: start,
        destination: end,
        travelMode: 'TRANSIT',// Mode : transport en commun (il existe aussi 'DRIVING')
        transitOptions: {
            modes: ['TRAIN'], // Moyen de transport : train
            departureTime: departureTime
        },
        region: 'fr',
        language: 'fr'


    };
    directionsService.route(request, function (result, status) {
        if (status == 'OK') {
            directionsRenderer.setDirections(result);
        }
    });
}

