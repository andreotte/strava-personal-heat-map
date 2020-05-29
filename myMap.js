window.onload = function() {
    initMap();
};

function initMap(){
    var mymap = L.map('mapid').setView([42.99, -85.66], 15); //Custom Input - Map center point and zoom level
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: //Custom Input - Mapbox access token 
    }).addTo(mymap);
    
    addRoutesToMap(routes, mymap);
}

function addRoutesToMap(routes, mymap){
    for(let i = 0; i < routes.length; i ++){
        var latLongs =  ""; 
        var polylineDecoded = L.Polyline.fromEncoded(routes[i])
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
