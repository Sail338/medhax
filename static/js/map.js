function initMap() {
    var map = new google.maps.Map(document.getElementById('map'),
    {
    zoom: 10,
    center: {lat: 26.1454529, lng: -80.7284561}
    });
	setMarkers(map);
}

function setMarkers(map) {
    $.get("/getAllVictims", function(data, status){
		console.log("data is" + data)

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
	data = JSON.parse(JSON.stringify(data))
    for (var i = 0; i < data.length; i++) {
        var marker = new google.maps.Marker({
            position: {lat: data[i].lat, lng: data[i].lng},
            map: map,
            icon: image,
            shape: shape
        });
    }
    });
}

function getCurrLoc() {
    if (navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };

        console.log(pos)
        var geocoder = new google.maps.Geocoder;
        geocoder.geocode({'location': pos}, function(results, status) {
        if (status === 'OK') {
            if (results[0]) {
                $("input[name=location]").val(results[0].formatted_address);
            }}
        
        });
    });
    }
}
