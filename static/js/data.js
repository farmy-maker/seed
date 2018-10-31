$(document).ready(function() {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('data', function(data) {
      Object.keys(data).forEach(function(key) {
          $('#current-' + key).text(data[key]);
        })
    });
});
