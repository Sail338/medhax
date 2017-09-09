function initMap() {
	var miami = {lat: 29.4700179, lng: -81.4759017}; 
	var map = new google.maps.Map(document.getElementById('map'), {
	  zoom: 10,
	  center: miami
	});
	var marker = new google.maps.Marker({
	  position: miami,
	  map: map
	});
}
