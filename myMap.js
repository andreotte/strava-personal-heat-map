let routes = [
    //paste encoded routes as comma separates strings from Activities.txt
];
    
window.onload = function() {
    initMap();
};

function initMap(){
    var mymap = L.map('mapid').setView([42.99, -85.66], 18); //Set lat and lng of the map center and zoom level here
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: //mapbox access token here
    }).addTo(mymap);
    
    addRoutesToMap(routes, mymap);
}

function addRoutesToMap(routes, mymap){
    for(let i = 0; i < routes.length; i ++){
        var latLongs =  "";
        // var polyline = L.Polyline.fromEncoded(routes[i]).addTo(mymap);
        
        var polylineDecoded = L.Polyline.fromEncoded(routes[i])
        // var polylineDecoded = polyline.decode(routes[i]);
        var modulus = Math.ceil(polylineDecoded._latlngs.length / 100);

        var snappedCoords = polylineDecoded._latlngs;
        for(var j = 0; j < polylineDecoded._latlngs.length; j ++)
        {
            if(j % modulus == 0){
                latLongs += snappedCoords[j].lng + ',' + snappedCoords[j].lat + ';'
            }
        }

        polylineDecoded.addTo(mymap);
        polylineDecoded.bringToFront();
    }
}
