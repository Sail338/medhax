function initMap() {
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 10,
          center: {lat: 29.4700179, lng: -81.4759017}
        });

        setMarkers(map);
      }

      // Data for the markers consisting of a name, a LatLng and a zIndex for the
      // order in which these markers should display on top of each other.
      var victims = [
        ['Alice', 29.597835, -81.226491, 4],
        ['Ranga', 29.5681124,-81.2015255, 5],
        ['Srihari', 29.5481124,-81.2415255, 3],
        ['Srigod', 29.5281124,-81.2615255, 2],
        ['Raj', 29.2674263,-81.0647543, 1]
      ];

      function setMarkers(map) {
        // Adds markers to the map.

        // Marker sizes are expressed as a Size of X,Y where the origin of the image
        // (0,0) is located in the top left of the image.

        // Origins, anchor positions and coordinates of the marker increase in the X
        // direction to the right and in the Y direction down.
        var image = {
          url: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
          // This marker is 20 pixels wide by 32 pixels high.
          size: new google.maps.Size(20, 32),
          // The origin for this image is (0, 0).
          origin: new google.maps.Point(0, 0),
          // The anchor for this image is the base of the flagpole at (0, 32).
          anchor: new google.maps.Point(0, 32)
        };
        // Shapes define the clickable region of the icon. The type defines an HTML
        // <area> element 'poly' which traces out a polygon as a series of X,Y points.
        // The final coordinate closes the poly by connecting to the first coordinate.
        var shape = {
          coords: [1, 1, 1, 20, 18, 20, 18, 1],
          type: 'poly'
        };
        for (var i = 0; i < victims.length; i++) {
          var victim = victims[i];
          var marker = new google.maps.Marker({
            position: {lat: victim[1], lng: victim[2]},
            map: map,
            icon: image,
            shape: shape,
            title: victim[0],
            zIndex: victim[3]
          });
        }
      }
