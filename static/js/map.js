function initMap() {
    var map = new google.maps.Map(document.getElementById('map'),
    {
    zoom: 10,
    center: {lat: 29.4700179, lng: -81.4759017}
    });
	setMarkers(map)
}

function setMarkers(map) {
    $.get("/getAllVictims", function(data, status){

    var image = {
        url: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
        size: new google.maps.Size(20, 32),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32)
    };
    var shape = {
        coords: [1, 1, 1, 20, 18, 20, 18, 1],
        type: 'poly'
    };
    for (var i = 0; i < data.length; i++) {
        var marker = new google.maps.Marker({
            position: {lat: data[i][0], lng: data[i][1]},
            map: map,
            icon: image,
            shape: shape,
            title: "test",
            zIndex: 1
        });
    }
    });
}


